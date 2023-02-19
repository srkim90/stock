import threading
import time
from typing import List, Tuple

from common.define import REDIS_WORKER_TH
from redis_db.redis_db import RedisDB


class RedisWorker:
    worker: List[RedisDB]
    lock: threading.Semaphore
    data_pair: List[Tuple[str, any, any]]

    def __init__(self, ipaddr: str, port: int, passwd: str) -> None:
        super().__init__()
        self.worker = []
        self.lock = threading.Semaphore(1)
        self.data_pair = []
        for idx in range(REDIS_WORKER_TH):
            self.worker.append(RedisDB(ipaddr, port, passwd))
            h_thread = threading.Thread(target=self.__worker_th, args=(idx,))
            h_thread.daemon = True
            h_thread.start()

    def put(self, key: str, data: any, data_class: any = None) -> None:
        self.__put_data(key, data, data_class)

    def __get_data(self) -> Tuple[str, any, any]:
        key = ""
        data = None
        data_class = None
        self.lock.acquire()
        if len(self.data_pair) == 0:
            self.lock.release()
            return key, data, data_class
        key, data, data_class = self.data_pair.pop(0)
        self.lock.release()
        return key, data, data_class

    def __put_data(self, key: str, data: any, data_class: any = None) -> None:
        self.lock.acquire()
        self.data_pair.append((key, data, data_class))
        self.lock.release()

    def __worker_th(self, idx):
        h_redis = self.worker[idx]
        while True:
            key, data, data_class = self.__get_data()
            if data is None:
                time.sleep(0.1)
                continue
            h_redis.put(key, data, data_class=data_class)
