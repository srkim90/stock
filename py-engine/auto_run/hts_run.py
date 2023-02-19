import os
import threading
import time
from typing import Union

from auto_run.key_input import keyInput, tabInput, press_paste
from auto_run.window_mgr import WindowMgr
from common.utils import sa_log


def _hts_set_foreground(wind_name, is_print=False):
    w = WindowMgr()
    w.find_window_wildcard(wind_name)
    handle = w.set_foreground()
    if is_print == True:
        w.print_window_list()

    return handle


class HtsRun:
    def __init__(self, hts_path, user_id, comm_passwd, auth_passwd, params=None):
        self.run_count = 0
        self.params = ""
        self.hts_path = hts_path

        self.user_id = user_id
        self.comm_passwd = comm_passwd
        self.auth_passwd = auth_passwd

        params = params if params is not None else []
        for param in params:
            self.params += param

    def __close_old_popup(self):
        self.__sleep(0.5)
        _hts_set_foreground("ncStarter")
        keyInput("N")

        self.__sleep(0.5)
        _hts_set_foreground("CYBOS FAMILY", is_print=False)
        keyInput("Y")

    def __run_proc_async(self, full_path):
        h_thread = threading.Thread(target=self.__app_proc, args=(full_path,))
        h_thread.daemon = True
        h_thread.start()

    @staticmethod
    def __hts_close_window(wind_name):
        w = WindowMgr()
        w.find_window_wildcard(wind_name)
        w.close_window()

    def __app_proc(self, full_path):
        self.run_count += 1
        os.system(full_path)
        self.run_count -= 1

    def _hts_set_account_info(self, user_id, comm_passwd, auth_passwd):
        w = WindowMgr()
        w.find_window_wildcard("CYBOS Starter")
        w.set_foreground()
        w.find_child_window_wildcard("Call Center")
        w.set_foreground()
        self.__sleep(0.5)
        tabInput()
        self.__sleep(0.5)
        press_paste(user_id)
        self.__sleep(0.5)
        tabInput()
        self.__sleep(0.5)
        press_paste(comm_passwd)
        self.__sleep(0.5)
        # tabInput()
        self.__sleep(1.5)
        press_paste(auth_passwd)
        self.__sleep(0.5)
        w.find_child_window_wildcard("연결")
        self.__sleep(0.5)
        keyInput("enter")
        self.__sleep(0.5)

    @staticmethod
    def __sleep(n_sleep: Union[int, float]):
        if type(n_sleep) == int:
            n_sleep = float(n_sleep)
        now_sleep = 0.0
        last_print = 0.0
        while n_sleep > now_sleep:
            sleep_unit = 0.1
            time.sleep(sleep_unit)
            now_sleep += sleep_unit
            last_print += sleep_unit
            if last_print >= 1.0:
                last_print = 0.0
                sa_log("sleep %f of %f" % (now_sleep, n_sleep))

    def run_hts(self):

        self.__close_old_popup()
        self.__close_old_popup()

        self.__sleep(60)
        full_path = "%s %s" % (self.hts_path, self.params)
        sa_log("full_path: %s" % (full_path))
        self.__run_proc_async(full_path)
        self.__sleep(30)
        sa_log("Check : ncStarter")
        _hts_set_foreground("ncStarter")
        keyInput("enter")
        self.__sleep(30)
        sa_log("Check : SYBOS FAMILY")
        _hts_set_foreground("CYBOS FAMILY", is_print=False)
        keyInput("enter")
        self.__sleep(45)

        sa_log("Check : Main Login")
        h_wnd = _hts_set_foreground("CYBOS Starter", is_print=False)
        if h_wnd is None:
            return

        self.__sleep(30)
        self._hts_set_account_info(self.user_id, self.comm_passwd, self.auth_passwd)

        self.__sleep(130)
        print("Check : Close Window")
        self.__hts_close_window("공지사항")
        self.__sleep(1)
        self.__hts_close_window("Internet Exp")
        self.__sleep(1)

        self.__close_old_popup()
        self.__close_old_popup()
