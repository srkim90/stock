# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : main.py
  Release  : 1
  Date     : 2018-09-28
 
  Description : Stock Win32 Autorun Main module
 
  Notes :
  ===================
  History
  ===================
  2018/09/28  created by Kim, Seongrae
'''
import datetime
import time
import sys



sys.path.append("Z://")
from auto_run.secure_provider import get_cybos_secure
from auto_run.hts_run import HtsRun
from common.utils import sa_log


def main():
    hts_path = "C:\\DAISHIN\\STARTER\\ncStarter.exe"
    user_id, comm_passwd, auth_passwd = get_cybos_secure()

    hts = HtsRun(hts_path, user_id, comm_passwd, auth_passwd, params=["/prj:cp"])
    while True:
        time.sleep(10)
        now_time = datetime.datetime.now()
        #if 4 < now_time.hour < 7:
        #    continue
        hts.run_hts()
        sa_log("Run HTS complete")
        time.sleep(30)
        return


if __name__ == "__main__":
    main()
