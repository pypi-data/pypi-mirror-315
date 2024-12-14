import queue
import re

from pathlib import Path
from typing import Any, Optional, Union, List
from importlib.metadata import version, PackageNotFoundError, requires

from PyQt6 import QtCore
from PyQt6.QtCore import QSettings, QIODeviceBase, pyqtSlot, QThread
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QStyle
from quiettransfer import protocols

from .FmWindow import Ui_FmTransfer
from .Worker import WorkerQuietSendQT, ReadQueue, WorkerGgSendQT, WorkerQuietReceiveQT, WorkerGgReceiveQT


class FmTransferWindow(QMainWindow, Ui_FmTransfer):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._qthread_print_line: Optional[QThread] = None
        self._qthread: Optional[QThread] = None
        self._print_line = None
        self._gg_present = True

        try:
            v = version("gg-transfer").split(".")
            vv = int(v[0]) * 100 + int(v[1]) * 10 + int(v[2])
            r = str(requires("fm-transfer"))
            m = re.findall(r'gg-transfer *([<=>]{1,2})(\d+)\.(\d+)\.(\d+)', r)
            m = m[0]
            if len(m) > 0:
                i = int(m[1]) * 100 + int(m[2]) * 10 + int(m[3])
                if not eval(f"{vv} {m[0]} {i}"):
                    self._gg_present = False
        except (PackageNotFoundError, IndexError, ValueError):
            self._gg_present = False

        self._mqueue = queue.Queue()
        self._worker_thread: Union[WorkerGgSendQT, WorkerQuietSendQT, WorkerQuietReceiveQT, WorkerGgReceiveQT, None] = None
        self._show_signals_in_log = False
        self._tool = True
        self._zlb = False
        self._quiet_protocol_list = list(protocols)
        self._quiet_protocol = 0
        self._gg_protocol = 2
        self._logic = False
        self._qserialports: List[Union[QSerialPortInfo, None]] = [None]
        self.setupUi(FmTransfer=self)  # type: ignore[no-untyped-call]
        pixmapi = QStyle.StandardPixmap.SP_FileDialogListView
        style = self.style()
        if style is not None:
            icon = style.standardIcon(pixmapi)
            self.setWindowIcon(icon)
        self._serialdevice: Optional[QSerialPort] = None
        self._serial = ""
        self._serial_index = 0
        self._serial_closed = True
        self._com_ports = ["none"]
        self.recheck_serial_ports()
        self.pttPressedRadioButton.toggled['bool'].connect(self.led.setOn)
        self.pttGroupBox.setDisabled(True)
        self.signalGroupBox.setDisabled(True)
        self.checkSignalButton.setDisabled(True)
        self.led.setDisabled(True)
        self._ptt_unpressed: bool = True
        self._signal_dtr = True  # DSR, True = RTS
        self._send_filename: Optional[str] = None
        self._receive_filename: Optional[str] = None
        self._receive_in_progress = False
        self._send_in_progress = False
        self._receive_in_progress_msg = False
        self._send_in_progress_msg = False
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self._pieces = 1
        self._current_piece = 0
        self._load_settings()

    def closeEvent(self, event: Optional[QCloseEvent]) -> None:
        self._save_settings()
        super().closeEvent(event)

    def _save_settings(self) -> None:
        settings = QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "fm-transfer",
                             "fm-transfer")
        settings.setValue("FmTransfer/geometry", self.saveGeometry())
        settings.setValue("FmTransfer/state", self.saveState())
        if self._receive_filename is not None:
            settings.setValue("FmTransfer/receivefile", self._receive_filename)
        if self._send_filename is not None:
            settings.setValue("FmTransfer/sendfile", self._send_filename)
        settings.setValue("FmTransfer/tool", self._tool)
        settings.setValue("FmTransfer/quiet_protocol", self._quiet_protocol)
        settings.setValue("FmTransfer/gg_protocol", self._gg_protocol)
        settings.setValue("FmTransfer/signal", self._signal_dtr)
        settings.setValue("FmTransfer/serial", self._serial)
        settings.setValue("FmTransfer/serial_index", self._serial_index)
        settings.setValue("FmTransfer/signal_logic", not self._logic)
        settings.setValue("FmTransfer/zlib", self._zlb)
        settings.setValue("FmTransfer/show_signals", self._show_signals_in_log)

    def _load_settings(self) -> None:
        settings = QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "fm-transfer",
                             "fm-transfer")
        self.restoreGeometry(settings.value("FmTransfer/geometry", self.saveGeometry()))
        self.restoreState(settings.value("FmTransfer/state", self.saveState()))

        show_signals = settings.value("FmTransfer/show_signals", self._show_signals_in_log, bool)
        self.actionShow_signals_in_log.setChecked(show_signals)
        if not self._show_signals_in_log:
            self.toggle_signals_in_log(show_signals)

        send_filename = settings.value("FmTransfer/sendfile", None)
        if send_filename is not None:
            self._send_filename = send_filename
            assert self._send_filename is not None
            short_fname = ('...' + self._send_filename[-40:]) if len(
                self._send_filename) > 40 else self._send_filename
            self.sendFileLineEdit.setText(short_fname)
        receive_filename = settings.value("FmTransfer/receivefile", None)
        if receive_filename is not None:
            self._receive_filename = receive_filename
            assert self._receive_filename is not None
            short_fname = ('...' + self._receive_filename[-40:]) if len(
                self._receive_filename) > 40 else self._receive_filename
            self.receiveFileLineEdit.setText(short_fname)

        self._tool = settings.value("FmTransfer/tool", self._tool, bool) if self._gg_present else self._gg_present
        self.quietRadioButton.setChecked(not self._tool)
        if self._tool:
            self.set_tool(self._tool)
        if not self._gg_present:
            self.ggRadioButton.setDisabled(True)
            self.sendMsgButton.setDisabled(True)
            self.recvMsgButton.setDisabled(True)
            self.shortMsg.setDisabled(True)

        gg_protocol = settings.value("FmTransfer/gg_protocol", self._gg_protocol, int)
        self.ggProtocolComboBox.setCurrentIndex(gg_protocol)
        quiet_protocol = settings.value("FmTransfer/quiet_protocol", self._quiet_protocol, int)
        self.quietProtocolComboBox.setCurrentIndex(quiet_protocol)

        self._zlb = settings.value("FmTransfer/zlib", self._zlb, bool)
        self.zlibCheckBox.setChecked(self._zlb)

        self._logic = settings.value("FmTransfer/signal_logic", self._logic, bool)
        self.signalLogic.setChecked(self._logic)
        self.set_signal_logic(self._logic)

        sign = settings.value("FmTransfer/signal", self._signal_dtr, bool)
        self._signal_dtr = sign
        self.rtsRadioButton.setChecked(not self._signal_dtr)
        self.toggle_signal(self._signal_dtr)

        serial_name = settings.value("FmTransfer/serial", "")
        serial_index = settings.value("FmTransfer/serial_index", self._serial_index, int)
        if serial_index < len(self._com_ports):
            if self._com_ports[serial_index] == serial_name:
                self.serialComboBox.setCurrentIndex(serial_index)

    def _disable_interface_elements(self, mode: str) -> None:

        self.checkSignalButton.setDisabled(True)
        self.recheckSerialButton.setDisabled(True)

        self.led.setDisabled(True)

        self.protocolGroupBox.setDisabled(True)
        self.pttGroupBox.setDisabled(True)
        self.signalGroupBox.setDisabled(True)
        self.toolGroupBox.setDisabled(True)

        self.serialComboBox.setDisabled(True)

        self.shortMsg.setDisabled(True)

        self.chooseSendFileButton.setDisabled(True)
        self.chooseRecvFileButton.setDisabled(True)

        if mode == "send_file":
            self.sendFileButton.setText("Stop sending")
            self.receiveButton.setDisabled(True)
            self.sendMsgButton.setDisabled(True)
            self.recvMsgButton.setDisabled(True)
        elif mode == "receive_file":
            self.sendFileButton.setDisabled(True)
            self.receiveButton.setText("Stop receiving")
            self.sendMsgButton.setDisabled(True)
            self.recvMsgButton.setDisabled(True)
        elif mode == "send_msg":
            self.sendFileButton.setDisabled(True)
            self.receiveButton.setDisabled(True)
            self.sendMsgButton.setText("Stop...")
            self.recvMsgButton.setDisabled(True)
        elif mode == "receive_msg":
            self.sendFileButton.setDisabled(True)
            self.receiveButton.setDisabled(True)
            self.sendMsgButton.setDisabled(True)
            self.recvMsgButton.setText("Stop...")
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def _enable_interface_elements(self) -> None:

        self.checkSignalButton.setDisabled(not self._show_signals_in_log or self._serial_closed)
        self.recheckSerialButton.setDisabled(False)

        self.led.setDisabled(self._serial_closed)

        self.protocolGroupBox.setDisabled(False)
        self.pttGroupBox.setDisabled(self._serial_closed)
        self.signalGroupBox.setDisabled(self._serial_closed)
        self.toolGroupBox.setDisabled(False)

        self.serialComboBox.setDisabled(False)
        if self._gg_present:
            self.shortMsg.setDisabled(False)

        self.chooseSendFileButton.setDisabled(False)
        self.chooseRecvFileButton.setDisabled(False)

        _trans = QtCore.QCoreApplication.translate
        self.sendFileButton.setText(_trans("FmTransfer", "Send file"))
        self.receiveButton.setText(_trans("FmTransfer", "Receive file"))
        self.recvMsgButton.setText(_trans("FmTransfer", "Receive"))
        self.sendMsgButton.setText(_trans("FmTransfer", "Send"))

        self.sendFileButton.setDisabled(False)
        self.receiveButton.setDisabled(False)
        if self._gg_present:
            self.sendMsgButton.setDisabled(False)
            self.recvMsgButton.setDisabled(False)

    def _send_msg_data_started(self) -> None:
        self._send_in_progress_msg = True
        self._pieces = 1
        self._current_piece = 0
        self.progressBar.setMaximum(self._pieces)
        self.progressBar.setValue(self._current_piece)
        self._disable_interface_elements("send_msg")
        self.messages.insertPlainText(f"{"-" * 15} Sending text message {"-" * 15}\n")
        self.messages.ensureCursorVisible()

    def _send_msg_data_end(self) -> None:
        self._send_in_progress_msg = False
        self._current_piece = 1
        self.progressBar.setValue(self._current_piece)
        self._enable_interface_elements()
        if not self._serial_closed and self.pttGroupBox.isEnabled():
            self.pttReleasedRadioButton.setChecked(True)

    def _receive_msg_data_started(self) -> None:
        self._receive_in_progress_msg = True
        self._pieces = 1
        self._current_piece = 0
        self.progressBar.setMaximum(self._pieces)
        self.progressBar.setValue(self._current_piece)
        self._disable_interface_elements("receive_msg")
        self.messages.insertPlainText(f"{"-" * 15} Receiving text message {"-" * 15}\n")
        self.messages.ensureCursorVisible()

    def _receive_msg_data_end(self) -> None:
        self._receive_in_progress_msg = False
        self._current_piece = 1
        self.progressBar.setValue(self._current_piece)
        self._enable_interface_elements()
        if not self._serial_closed and self.pttGroupBox.isEnabled():
            self.pttReleasedRadioButton.setChecked(True)

    def _send_data_started(self) -> None:
        self._pieces = 1
        self._current_piece = 0
        self._send_in_progress = True
        self.progressBar.setMaximum(self._pieces)
        self.progressBar.setValue(self._current_piece)
        self._disable_interface_elements("send_file")
        self.messages.insertPlainText(f"{"-" * 15} Sending file {"-" * 15}\n")
        self.messages.ensureCursorVisible()

    def _send_data_end(self) -> None:
        self._send_in_progress = False
        self._enable_interface_elements()
        if not self._serial_closed and self.pttGroupBox.isEnabled():
            self.pttReleasedRadioButton.setChecked(True)

    def _receive_data_started(self) -> None:
        self._receive_in_progress = True
        self._pieces = 1
        self._current_piece = 0
        self.progressBar.setMaximum(self._pieces)
        self.progressBar.setValue(self._current_piece)
        self._disable_interface_elements("receive_file")
        self.messages.insertPlainText(f"{"-" * 15} Receiving file {"-" * 15}\n")
        self.messages.ensureCursorVisible()

    def _receive_data_end(self) -> None:
        self._receive_in_progress = False
        self._enable_interface_elements()
        if not self._serial_closed and self.pttGroupBox.isEnabled():
            self.pttReleasedRadioButton.setChecked(True)

    # noinspection PyUnresolvedReferences
    @pyqtSlot(int)
    def reinit_serial(self, index: int) -> None:
        self._serial_index = index
        if self._serialdevice and not self._serial_closed: # and self._serialdevice.is_open:
            self.pttReleasedRadioButton.setChecked(True)
            self._serialdevice.close()
            self._serialdevice = None
            self._serial_closed = True
            self.pttGroupBox.setDisabled(True)
            self.signalGroupBox.setDisabled(True)
            self.checkSignalButton.setDisabled(True)
            self.led.setDisabled(True)
        if self._serial_index != 0:
            self._serial = self._com_ports[self._serial_index]
            self._serialdevice = QSerialPort(self._qserialports[index], self)
            self._serialdevice.setBaudRate(9600)
            try:
                result = self._serialdevice.open(QIODeviceBase.OpenModeFlag.ReadWrite)
                if not result:
                    raise IOError(f"ERROR: {self._serialdevice.portName()},"
                                  f" {self._serialdevice.errorString()}")
                self._serialdevice.setRequestToSend(self._logic)
                self._serialdevice.setDataTerminalReady(self._logic)
                self._serial_closed = False
                self.pttGroupBox.setDisabled(False)
                self.signalGroupBox.setDisabled(False)
                self.led.setDisabled(False)
                self.checkSignalButton.setDisabled(not self._show_signals_in_log or self._serial_closed)
                self._send_signal()
                self.check_signal()
            except IOError as e:
                self.messages.insertPlainText(str(e) + "\n")
                self.messages.ensureCursorVisible()
                self.serialComboBox.setCurrentIndex(0)
            except Exception as e:
                self.messages.insertPlainText(str(e) + "\n")
                self.messages.ensureCursorVisible()
                self.serialComboBox.setCurrentIndex(0)

    # noinspection PyUnresolvedReferences
    def _send_signal(self) -> None:
        if self._serialdevice and not self._serial_closed:
            if self._ptt_unpressed:
                self._serialdevice.setRequestToSend(self._logic)
                self._serialdevice.setDataTerminalReady(self._logic)
            else:
                if self._signal_dtr:
                    self._serialdevice.setDataTerminalReady(not self._logic)
                    self._serialdevice.setRequestToSend(self._logic)
                else:
                    self._serialdevice.setDataTerminalReady(self._logic)
                    self._serialdevice.setRequestToSend(not self._logic)

    @pyqtSlot()
    def check_signal(self) -> None:
        if self._show_signals_in_log:
            # noinspection PyUnresolvedReferences
            if self._serialdevice and not self._serial_closed:
                if self._serialdevice.isDataTerminalReady():
                    self.messages.insertPlainText("DTR signal DOWN\n")
                else:
                    self.messages.insertPlainText("DTR signal UP\n")
                if self._serialdevice.isRequestToSend():
                    self.messages.insertPlainText("RTS signal DOWN\n")
                else:
                    self.messages.insertPlainText("RTS signal UP\n")
            self.messages.ensureCursorVisible()

    @pyqtSlot(bool)
    def toggle_ptt(self, checked: bool) -> None:
        # noinspection PyUnresolvedReferences
        if not self._serial_closed:
            self._ptt_unpressed = checked
            self._send_signal()
            self.check_signal()

    @pyqtSlot(bool)
    def toggle_signal(self, sign: bool) -> None:
        # noinspection PyUnresolvedReferences
        if not self._serial_closed:
            self._signal_dtr = sign
            self._send_signal()
            self.check_signal()

    @pyqtSlot()
    def recheck_serial_ports(self) -> None:
        if not self._serial_closed and isinstance(self._serialdevice, QSerialPort):
            self.pttReleasedRadioButton.setChecked(True)
            self.pttGroupBox.setDisabled(True)
            self.signalGroupBox.setDisabled(True)
            self.checkSignalButton.setDisabled(True)
            self.led.setDisabled(True)
            self._serialdevice.close()
            self._serial_closed = True
            self._serial = ""
            self._serialdevice = None
        try:
            self.serialComboBox.currentIndexChanged.disconnect(self.reinit_serial)
        except TypeError:
            pass
        self._qserialports = [None]
        self.serialComboBox.clear()
        self._com_ports = ["none"]
        self.serialComboBox.addItem("Choose a serial port...")
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            self._com_ports.append(port.systemLocation())
            self._qserialports.append(port)
            self.serialComboBox.addItem(port.systemLocation())
        self.serialComboBox.currentIndexChanged.connect(self.reinit_serial)

    def thread_ended_callback(self) -> None:
        if self._send_in_progress:
            self._send_data_end()
        elif self._receive_in_progress:
            self._receive_data_end()
        elif self._send_in_progress_msg:
            self._send_msg_data_end()
        elif self._receive_in_progress_msg:
            self._receive_msg_data_end()

    def _print_from_queue(self, line: str):
        if line.startswith("Size:"):
            match = re.match(r"Size: (\d+)", line)
            if match is not None:
                self._pieces = int(match.group(1))
                self.progressBar.setMaximum(self._pieces)
            self.messages.insertPlainText(line + "\n")
        elif line.startswith("Sent:"):
            match = re.match(r"Sent: (\d+)", line)
            if match is not None:
                self._current_piece = int(match.group(1))
                self.progressBar.setValue(self._current_piece)
        elif line.startswith("Pieces: "):
            match = re.match(r"Pieces: (\d+)", line)
            if match is not None:
                self._pieces = int(match.group(1))
                self.progressBar.setMaximum(self._pieces)
        elif line.startswith("Piece "):
            match = re.match(r"Piece (\d+)", line)
            if match is not None:
                self._current_piece = int(match.group(1))
                self.progressBar.setValue(self._current_piece)
        elif line.startswith("Received:"):
            match = re.match(r"Received: (\d+).*", line)
            if match is not None:
                self._current_piece = int(match.group(1))
                self.progressBar.setValue(self._current_piece)
        elif line.startswith("Got header"):
            match = re.search(r"(\d+)$", line)
            if match is not None:
                self._pieces = int(match.group(1))
                self.progressBar.setMaximum(self._pieces)
                self.messages.insertPlainText(line + "\n")
        elif line.startswith("CRC") or line.startswith("Sending") or line.startswith("Time") or line.startswith("Speed") or line.find("ERROR") != -1 or line.find("Error") != -1:
            self.messages.insertPlainText(line + "\n")
        elif line.startswith(": "):
            self.messages.insertPlainText(f"Received text message: {line[2:]}\n")
            self.shortMsg.setText(line[2:])
        elif line.startswith(":: "):
            self.messages.insertPlainText(f"Text message sent: {line[3:]}\n")
        self.messages.ensureCursorVisible()

    def _start_threads(self, operation: str) -> None:

        self._mqueue = queue.Queue()
        if operation == "receive_quiet":
            self._worker_thread = WorkerQuietReceiveQT(mqueue=self._mqueue, zlb=self._zlb, output=self._receive_filename, overwrite=True, protocol=self._quiet_protocol_list[self._quiet_protocol], file_transfer=True)
        elif operation == "send_quiet":
            self._worker_thread = WorkerQuietSendQT(mqueue=self._mqueue, zlb=self._zlb, input_file=self._send_filename, protocol=self._quiet_protocol_list[self._quiet_protocol], file_transfer=True)
        elif operation == "receive_gg":
            self._worker_thread = WorkerGgReceiveQT(output_file=self._receive_filename, overwrite=True, file_transfer=True, mqueue=self._mqueue)
        elif operation == "send_gg":
            self._worker_thread = WorkerGgSendQT(inputfile=self._send_filename, protocol=self._gg_protocol, file_transfer=True, mqueue=self._mqueue)
        elif operation == "receive_gg_msg":
            self._worker_thread = WorkerGgReceiveQT(mqueue=self._mqueue, getdata=True)
        elif operation == "send_gg_msg":
            self._worker_thread = WorkerGgSendQT(protocol=self._gg_protocol, mqueue=self._mqueue, msg=self.shortMsg.text())
        else:
            raise ValueError("Unknown operation")

        # One
        self._qthread = QThread()
        self._worker_thread.moveToThread(self._qthread)
        # self._worker_thread.finished_signal.connect(self.thread_ended_callback)
        self._worker_thread.finished_signal.connect(self.thread_ended_callback)
        self._worker_thread.finished_signal.connect(self._qthread.quit)
        # noinspection PyUnresolvedReferences
        self._qthread.started.connect(self._worker_thread.go)
        # noinspection PyUnresolvedReferences
        self._qthread.finished.connect(self._qthread.deleteLater)
        # noinspection PyUnresolvedReferences
        self._qthread.finished.connect(self._worker_thread.deleteLater)

        # Two
        self._qthread_print_line = QThread()
        self._print_line = ReadQueue(self._mqueue)
        self._print_line.moveToThread(self._qthread_print_line)
        self._print_line.strReady.connect(self._print_from_queue)
        # self._print_line.finished_signal.conncet(self._print_line.deleteLater)
        self._print_line.finished_signal.connect(self._qthread_print_line.quit)
        # noinspection PyUnresolvedReferences
        self._qthread_print_line.started.connect(self._print_line.getstring)
        # noinspection PyUnresolvedReferences
        self._qthread_print_line.finished.connect(self._qthread_print_line.deleteLater)
        # noinspection PyUnresolvedReferences
        self._qthread_print_line.finished.connect(self._print_line.deleteLater)
        self._qthread.start()
        self._qthread_print_line.start()

    @pyqtSlot()
    def send_file(self) -> None:
        if not self._send_in_progress:
            if not self._send_filename or not Path(self._send_filename).is_file():
                self.choose_send_file()
            if self._send_filename is not None and Path(self._send_filename).is_file():
                if not self._serial_closed and self.pttGroupBox.isEnabled():
                    self.pttPressedRadioButton.setChecked(True)
                self._send_data_started()
                if self._tool:
                    self._start_threads("send_gg")
                else:
                    self._start_threads("send_quiet")
        else:
            if self._send_in_progress and self._qthread.isRunning():
                self.sendFileButton.setDisabled(True)
                self._mqueue.put("ABORT")
                self._worker_thread.obj.stop(True)

    @pyqtSlot()
    def receive_file(self) -> None:
        if not self._receive_in_progress:
            if not self._receive_filename:
                self.choose_recv_file()
            if self._receive_filename:
                self._receive_data_started()
                if self._tool:
                    self._start_threads("receive_gg")
                else:
                    self._start_threads("receive_quiet")
        else:
            if self._receive_in_progress and self._qthread.isRunning():
                self.receiveButton.setDisabled(True)
                self._mqueue.put("ABORT")
                self._worker_thread.obj.stop(True)

    @pyqtSlot()
    def send_text(self) -> None:
        if not self._send_in_progress_msg:
            msg = self.shortMsg.text()
            if msg:
                if not self._serial_closed and self.pttGroupBox.isEnabled():
                    self.pttPressedRadioButton.setChecked(True)
                self._send_msg_data_started()
                self._start_threads("send_gg_msg")
        else:
            if self._send_in_progress_msg and self._qthread.isRunning():
                self.sendMsgButton.setDisabled(True)
                self._worker_thread.obj.stop(True)

    @pyqtSlot()
    def receive_text(self) -> None:
        if not self._receive_in_progress_msg:
            self._receive_msg_data_started()
            self._start_threads("receive_gg_msg")
        else:
            if self._receive_in_progress_msg and self._qthread.isRunning():
                self.recvMsgButton.setDisabled(True)
                self._worker_thread.obj.stop(True)

    @pyqtSlot(int)
    def set_gg_protocol(self, protocol: int) -> None:
        self._gg_protocol = protocol

    @pyqtSlot(int)
    def set_quiet_protocol(self, protocol: int) -> None:
        self._quiet_protocol = protocol

    @pyqtSlot(bool)
    def set_tool(self, tool: bool) -> None:
        self._tool = tool
        self.ggProtocolComboBox.setDisabled(not self._tool)
        self.zlibCheckBox.setDisabled(self._tool)
        self.quietProtocolComboBox.setDisabled(self._tool)

    @pyqtSlot()
    def choose_recv_file(self) -> None:
        file_dialog = QFileDialog(self, directory=str(Path(self._receive_filename).parent) if self._receive_filename is not None else ".")
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self._receive_filename = selected_files[0]
            short_fname = ('...' + self._receive_filename[-40:]) if len(
                self._receive_filename) > 40 else self._receive_filename
            self.receiveFileLineEdit.setText(short_fname)

    @pyqtSlot()
    def choose_send_file(self) -> None:
        file_dialog = QFileDialog(self, directory=str(Path(self._send_filename).parent) if self._send_filename is not None else ".")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self._send_filename = selected_files[0]
            short_fname = ('...' + self._send_filename[-40:]) if len(
                self._send_filename) > 40 else self._send_filename
            self.sendFileLineEdit.setText(short_fname)

    @pyqtSlot(bool)
    def set_signal_logic(self, logic: bool) -> None:
        self._logic = not logic
        self._send_signal()
        self.check_signal()

    @pyqtSlot(bool)
    def set_compression(self, compression: bool) -> None:
        self._zlb = compression

    @pyqtSlot()
    def save_config(self) -> None:
        self._save_settings()

    @pyqtSlot()
    def load_config(self) -> None:
        self._load_settings()

    @pyqtSlot()
    def clear_log(self) -> None:
        self.messages.clear()

    @pyqtSlot(bool)
    def toggle_signals_in_log(self, signals_in_log: bool) -> None:
        self._show_signals_in_log = signals_in_log
        self.checkSignalButton.setDisabled(not self._show_signals_in_log or self._serial_closed)
