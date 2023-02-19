import datetime
import os
import sys
import time

sys.path.append("Z://")
from cybos_downloader.inquire_cybos_stock_mst2 import InquireCybosStockMst2

from common.utils import sa_log

is_reboot = True
is_check_forever = False


def check_params():
    global is_reboot
    global is_check_forever
    sa_log("input : %s" % sys.argv[1:])
    for param in sys.argv[1:]:
        if "test" in param.lower():
            sa_log("enable TEST Mode")
            is_reboot = False
        elif "forever" in param.lower():
            sa_log("enable FOREVER Mode")
            is_check_forever = True


def check():
    now_time = datetime.datetime.now()
    e = InquireCybosStockMst2(market="test")
    hour = now_time.hour
    if e.test() is False:
        sa_log("TEST FAIL!!")
        if 3 <= now_time.hour <= 17:
            sa_log(" -- TRY REBOOT")
            if is_reboot is True:
                for idx in range(10):
                    time.sleep(1.0)
                    sa_log("System reboot in : %d sec" % idx)
                os.system("shutdown -r")
        else:
            sa_log(" -- NOT REBOOT")
            while True:
                time.sleep(1)
    else:
        sa_log("TEST OK!!")


def main():
    check_params()
    while True:
        check()
        if is_check_forever is False:
            break
        time.sleep(360)


if __name__ == "__main__":
    main()
