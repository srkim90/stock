import threading
import time


class StockLock:
    n_works: int
    threshold: int
    lock: threading.Semaphore

    def __init__(self, threshold: int) -> None:
        self.n_works = 0
        self.threshold = threshold
        self.lock = threading.Semaphore(1)
        super().__init__()

    def increase(self):
        self.lock.acquire()
        self.n_works += 1
        self.lock.release()

    def decrease(self):
        self.lock.acquire()
        self.n_works -= 1
        self.lock.release()

    def wait(self):
        self.lock.acquire()
        n_works = self.n_works
        self.lock.release()
        while n_works > self.threshold:
            self.lock.acquire()
            n_works = self.n_works
            self.lock.release()
            time.sleep(0.1)
