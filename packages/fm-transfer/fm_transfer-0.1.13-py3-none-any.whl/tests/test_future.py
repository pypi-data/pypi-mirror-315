import multiprocessing
import sys
import unittest
from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing.queues import Queue
from time import sleep
import os
from unittest import skip
from multiprocessing.pool import Pool, AsyncResult
import signal
from queue import Empty


class FutureTest(unittest.TestCase):
    @skip("Skipping pool executor test")
    def test_processpoolexecutor(self):
        e = ProcessPoolExecutor(max_workers=1)
        f = MyWorkerAndCallbacks()
        future = e.submit(f.slow_task, float(4))
        future.add_done_callback(self.process_end_callback)
        a = 0
        while not future.done():
            print(f"{a}")
            a += 1
            sleep(0.5)
        sleep(1)
        self.assertEqual(future.result(), "Done!")  # add assertion here

    def process_end_callback(self, future):
        print(f"In callback: future result = '{future.result()}'\nIn callback: slow task ended!")


class MyWorkerAndCallbacks:

    def __init__(self):
        self.pid = -1

    def slow_task(self, secs: float) -> str:
        self.pid = os.getpid()
        print(f"{self.pid}: {secs}")
        with open(r"r:\pid", "w") as f:
            f.write(str(os.getpid()))
        sleep(secs)
        return "Done!"

    def printing_task(self, secs: int) -> str:
        self.pid = os.getpid()
        print(f"{self.pid}: {secs}")
        with open(r"r:\pid", "w") as f:
            f.write(str(os.getpid()))
        for i in range(secs):
            sleep(1)
            print(f"{i}: {os.getpid()}")
        return "Done!"

    def process_end_callback(self, future):
        # print(f"In callback: future result = '{future.result()}'\nIn callback: slow task ended!")
        pass

    def process_end_ok(self, res):
        print(f"Pool process end ok: {res}")
        # print(f"In callback: future result = '{future.result()}'\nIn callback: slow task ended!")

    def process_end_ko(self, res):
        print(f"Pool process end ko: {res}")


class StdoutQueue(Queue):

    def __init__(self,*args,**kwargs):
        ctx = multiprocessing.get_context()
        super(StdoutQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self,msg):
        self.put(msg)

    def flush(self):
        sys.__stdout__.flush()


class PoolTest(unittest.TestCase):
    p: Pool
    w: MyWorkerAndCallbacks
    a: AsyncResult
    q: StdoutQueue

    @skip("Skipping pool executor test")
    def test_pool(self):
        try:
            self.p = Pool(1, maxtasksperchild=100)
            self.w = MyWorkerAndCallbacks()
            self.a = self.p.apply_async(self.w.slow_task, args=[float(10)], callback=self.w.process_end_ok, error_callback=self.w.process_end_ko)
            sleep(2)
            res = True
            with open(r"r:\pid", "r") as f:
                pid = int(f.read())
                print(pid)
            os.kill(pid, signal.CTRL_C_EVENT)
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt", e)
            res = False
        except OSError as e:
            print("OSError", e)
            res = False
        finally:
            self.p.close()
            # self.p.join()

        self.assertEqual(True, res)  # add assertion here

    def test_print(self):
        try:
            self.q = StdoutQueue()
            self.p = Pool(1, maxtasksperchild=100, initializer=self.pool_init, initargs=(self.q,))
            self.w = MyWorkerAndCallbacks()
            self.a = self.p.apply_async(self.w.printing_task, args=[int(50)], callback=self.w.process_end_ok, error_callback=self.w.process_end_ko)
            # sleep(2)
            res = True
            # with open(r"r:\pid", "r") as f:
            #     pid = int(f.read())
            #     print(pid)
            # os.kill(pid, signal.CTRL_C_EVENT)
            buf = ""
            while True:
                try:
                    line = self.q.get(timeout=10)
                    buf += line
                    if line.endswith("\n"):
                        print(buf, end="")
                        buf = ""
                    # line_b = line.encode("utf-8")
                    # print(line_b)
                except Empty:
                    break


        except KeyboardInterrupt as e:
            print("Keyboard Interrupt", e)
            res = False
        except OSError as e:
            print("OSError", e)
            res = False
        finally:
            self.p.close()
            # self.p.join()

        self.assertEqual(True, res)  # add assertion here

    @staticmethod
    def pool_init(q):
        sys.stdout = q

if __name__ == '__main__':
    unittest.main()
