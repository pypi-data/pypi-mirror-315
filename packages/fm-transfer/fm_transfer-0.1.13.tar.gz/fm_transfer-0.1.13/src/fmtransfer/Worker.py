import queue
import quiettransfer

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

try:
    # noinspection PyUnresolvedReferences
    import ggtransfer
except ImportError:
    pass


# noinspection PyUnresolvedReferences
class ReadQueue(QObject):

    strReady = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, mq: queue.Queue[str]):
        super().__init__()
        self._mq = mq

    @pyqtSlot()
    def getstring(self) -> None:
        while True:
            try:
                line = self._mq.get(timeout=1.0).strip("\n\r \t")
                self._mq.task_done()
                # print(f"-{line}-", flush=True)
                if line.startswith("ABORT"):
                    break
                self.strReady.emit(line)
                if line.startswith("Speed:") or line.startswith("Speed (payload only)") or line.find("ERROR") != -1 or line.find("Error") != -1:
                    break
            except queue.Empty:
                pass
        # print("exiting getstring thread")
        self.finished_signal.emit()


# noinspection PyUnresolvedReferences
class WorkerQuietSendQT(QObject):

    finished_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.obj = None

    @pyqtSlot()
    def go(self) -> None:
        try:
            self.obj = quiettransfer.SendFile(*self.args, **self.kwargs)
            self.obj.send_file()
        finally:
            # print("exiting quiet sender thread")
            self.finished_signal.emit()


# noinspection PyUnresolvedReferences
class WorkerGgSendQT(QObject):

    finished_signal = pyqtSignal()

    def __init__(self, *args, msg: str = None, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.obj = None
        self.msg = msg

    @pyqtSlot()
    def go(self) -> None:
        try:
            self.obj = ggtransfer.Sender(*self.args, **self.kwargs)
            self.obj.send(self.msg)
            if self.msg is not None:
                self.kwargs.get("mqueue").put(f":: {self.msg}", True)
                self.kwargs.get("mqueue").put("ABORT", True)
        finally:
            # print("exiting gg sender thread")
            self.finished_signal.emit()


# noinspection PyUnresolvedReferences
class WorkerQuietReceiveQT(QObject):

    finished_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.obj = None

    @pyqtSlot()
    def go(self) -> None:
        try:
            self.obj = quiettransfer.ReceiveFile(*self.args, **self.kwargs)
            self.obj.receive_file()
        finally:
            # print("exiting quiet receiver thread")
            self.finished_signal.emit()


# noinspection PyUnresolvedReferences
class WorkerGgReceiveQT(QObject):

    finished_signal = pyqtSignal()

    def __init__(self, *args, getdata: bool = False, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.obj = None
        self.getdata = getdata

    @pyqtSlot()
    def go(self) -> None:
        try:
            self.obj = ggtransfer.Receiver(*self.args, **self.kwargs)
            res = self.obj.receive(self.getdata)
            if self.getdata:
                if res is not None:
                    self.kwargs.get("mqueue").put(f": {res}", True)
                self.kwargs.get("mqueue").put("ABORT", True)

        finally:
            # print("exiting gg receiver thread")
            self.finished_signal.emit()
