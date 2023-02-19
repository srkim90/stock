import datetime
import gzip
import os
import threading
from typing import List


def make_dirs(path_list: List[str]):
    for path in path_list:
        if os.path.exists(path) is True:
            continue
        os.makedirs(path)


def get_now_yyyymmdd():
    return datetime.datetime.now().strftime("%Y%m%d")


def make_url(url: str) -> str:
    from common.define import OPEN_API_BASE_URL
    url = url.strip()
    if url[0] == "/":
        url = url[1:]
    return "%s/%s" % (OPEN_API_BASE_URL, url)


def get_uncompressed_size(file_name: str) -> int:
    with gzip.open(file_name, 'rb') as fd:
        fd.seek(0, 2)
        size = fd.tell()
    return size


log_lock = threading.Semaphore(1)


def sa_log(message: str):
    suffix = "%s[%-5s]:" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), os.getpid())
    log_lock.acquire()
    print("%s%s" % (suffix, message))
    log_lock.release()
