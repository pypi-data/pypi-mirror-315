import multiprocessing
import os
import queue
import sys
import tempfile
from multiprocessing.pool import Pool, ThreadPool
from multiprocessing.spawn import freeze_support
from threading import Thread
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class WorkerQuietSend:

    # def __init__(self, *args, clean: SharedMemoryManager.ShareableList = None, **kwargs):
    def __init__(self, *args, pidfile: str = None, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.pidfile = pidfile
        self.sender = None
        # self._signal = signal.SIGUSR1 if not sys.platform.startswith("win32") else signal.SIGFPE

    def send(self) -> bool:
        res = True
        # self.clean[0] = os.getpid()
        try:
            with open(self.pidfile, "w") as f:
                f.write(str(os.getpid()))
            print("send pid:", os.getpid())
            import quiettransfer
            self.sender = quiettransfer.SendFile(*self.args, **self.kwargs)
            # sendr._script = True
            res_int = self.sender.send_file()
            res = True if res_int == 0 else False
        except Exception as e:
            print("worker.py catched exception", e)
            res = False
        finally:
            return res


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.getter_thread = None
        self.async_r = None
        self.quiet_send = None
        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

        fdtempfile, self.pid_file = tempfile.mkstemp(text=False)
        os.close(fdtempfile)
        self.send_filename = __file__
        self.executor = ThreadPool(1)
        self.manager = multiprocessing.Manager()
        self.mqueue = self.manager.Queue()
        self.sending = False

    def button_clicked(self, s):
        print("click", s)
        if not self.sending:
            self.sending = True
            self.getter_thread = Thread(target=self.getter, args=(self.mqueue,))
            self.quiet_send = WorkerQuietSend(mqueue=self.mqueue, zlb=True, pidfile=self.pid_file, input_file=self.send_filename, protocol="audible", file_transfer=True)
            self.async_r = self.executor.apply_async(self.quiet_send.send, callback=self.callback, error_callback=self.error_callback)
            self.getter_thread.start()
        else:
            self.sending = False
            self.quiet_send.sender.stop(True)
            self.async_r.wait()
            self.mqueue.put("Speed")
            self.getter_thread.join()

        # async_r.wait()
        # getter_thread.join()

    def getter(self, tmqueue):
        try:
            keep = True
            while keep:
                line = tmqueue.get().strip("\n\r ")
                print(line)
                if line.startswith("Speed"):
                    keep = False
                    break
        except queue.Empty:
            print("empty")
        print("leaving getter")

    def callback(self, res):
        print(f"callback success: {res}")

    def error_callback(self, res):
        print(f"callback error: {res}")


if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
