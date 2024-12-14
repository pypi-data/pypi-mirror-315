import queue

import quiettransfer
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget


class ReadQueue(QObject):
    strReady = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, mq: queue.Queue, w):
        super().__init__()
        self.mq = mq
        self.w = w

    @pyqtSlot()
    def getstring(self):
        a = 0
        while a < 10:
            try:
                line = self.mq.get(timeout=1.0).strip("\n\r ")
                self.mq.task_done()
                print(line, flush=True)
                self.strReady.emit(line)
                if line.startswith("ABORT") or line.startswith("Speed:") or line.startswith("Speed (payload only)"):
                    print("exiting getstring thread")
                    break
            except queue.Empty as e:
                a += 1
                pass
        # self.mq.put("ABORT")
        self.w.receiver.stop(True)
        self.finished_signal.emit()


class WorkerQuietReceiveQT(QObject):

    finished_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.receiver = None

    @pyqtSlot()
    def receive(self):
        try:
            self.receiver = quiettransfer.ReceiveFile(*self.args, **self.kwargs)
            self.receiver.receive_file()
        finally:

            self.finished_signal.emit()
            print("exiting receiver thread")


class Worker(QObject):
    # Signal emitted when the task is complete
    finished_signal = pyqtSignal()

    @pyqtSlot()
    def do_work(self):
        # Simulate a long-running task
        # import time
        # time.sleep(2)  # Simulate work

        self.finished_signal.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.worker2 = None
        self.thread2 = None
        self.mqueue = None
        self.thread = None
        self.worker = None
        self.setWindowTitle("QObject Worker Example")
        self.resize(300, 200)

        self.label = QLabel("Press the button to start the worker")
        self.label2 = QLabel("Second Label")
        self.button = QPushButton("Start Worker")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Connect the button to start the worker
        self.button.clicked.connect(self.start_worker)

    def start_worker(self):
        # Create the worker and thread
        self.thread = QThread()
        self.thread2 = QThread()
        self.mqueue = queue.Queue()
        self.worker = WorkerQuietReceiveQT(mqueue=self.mqueue, zlb=False, output=r"r:\out.rx", overwrite=True, protocol="audible", file_transfer=True)
        self.worker2 = ReadQueue(self.mqueue, self.worker)

        # Move the worker to the thread
        self.worker.moveToThread(self.thread)
        self.worker2.moveToThread(self.thread2)


        # Connect signals and slots
        self.thread.started.connect(self.worker.receive)
        self.thread2.started.connect(self.worker2.getstring)
        self.worker.finished_signal.connect(self.on_worker_finished)
        self.worker.finished_signal.connect(self.thread.quit)
        self.worker2.finished_signal.connect(self.on_worker2_finished)
        self.worker2.finished_signal.connect(self.thread2.quit)
        self.worker2.strReady.connect(self.printline)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.thread2.finished.connect(self.worker2.deleteLater)

        # Start the thread
        self.thread.start()
        self.thread2.start()
        self.label.setText("Worker is running...")
        self.label2.setText("Worker2 is running...")

    def on_worker_finished(self):
        # Update the label when the worker finishes
        self.label.setText("Worker has finished!")
        print("Worker has finished!")

    def on_worker2_finished(self):
        # Update the label when the worker finishes
        self.label2.setText("Worker2 has finished!")
        print("Worker2 has finished!")

    def printline(self, line):
        print(line, flush=True)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
