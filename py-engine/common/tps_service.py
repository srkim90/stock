import datetime
import threading
import time
from typing import Dict, Tuple, List

from common.utils import sa_log

TPS_THRESHOLD = 10


class TpsService:
    tps_class_name: str
    tps_duration: Dict[int, list]  # List[int, datetime.datetime]

    def __init__(self, tps_class_name: str) -> None:
        super().__init__()
        self.tps_class_name = tps_class_name
        self.tps_duration = {
            1: [0, datetime.datetime.now()],
            # 5: [0, datetime.datetime.now()],
            # 10: [0, datetime.datetime.now()],
            # 30: [0, datetime.datetime.now()],
            # 60: [0, datetime.datetime.now()]
        }
        self.tps_lock = threading.Semaphore(1)
        h_thread = threading.Thread(target=self.__tps_thread)
        h_thread.daemon = True
        h_thread.start()

    def __tps_thread(self):
        while True:
            time.sleep(0.1)
            now_time = datetime.datetime.now()
            self.tps_lock.acquire()
            for duration in self.tps_duration.keys():
                n_call = self.tps_duration[duration][0]
                last_reset = self.tps_duration[duration][1]
                log_message = None
                if (now_time - last_reset).seconds >= duration:
                    self.tps_duration[duration][0] = 0
                    self.tps_duration[duration][1] = now_time
                    self.tps_lock.release()
                    log_message = "[%s] CALL=%d, Duration=%d TPS=%s" % (
                        self.tps_class_name, n_call, duration, n_call / duration)
                    self.tps_lock.acquire()
                if log_message is not None:
                    sa_log(log_message)

            self.tps_lock.release()

    def check(self):
        self.tps_lock.acquire()
        for duration in self.tps_duration.keys():
            self.tps_duration[duration][0] += 1
        self.tps_lock.release()


tps_init_lock = threading.Semaphore(1)
api_tps: TpsService = None
cybos_tps: TpsService = None


def inc_api_tps():
    global api_tps
    tps_init_lock.acquire()
    if api_tps is None:
        api_tps = TpsService("한투증권 API")
    tps_init_lock.release()
    api_tps.check()


def inc_cybos_tps():
    global cybos_tps
    tps_init_lock.acquire()
    if cybos_tps is None:
        cybos_tps = TpsService("Cybos API")
    tps_init_lock.release()
    cybos_tps.check()
