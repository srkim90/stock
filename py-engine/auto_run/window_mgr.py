# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : window_mgr.py
  Release  : 1
  Date     : 2018-09-28
 
  Description : Stock HTS window manager module
 
  Notes :
  ===================
  History
  ===================
  2018/09/28  created by Kim, Seongrae
'''

import win32con
# win32 module import
import win32gui

# common package import
from auto_run import key_input
# import win32com.client
from common.utils import sa_log


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        self.wind_list = []
        """Constructor"""
        self._handle = None
        self._child_handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        # print("call _child_window_enum_callback")
        w_name = str(win32gui.GetWindowText(hwnd))
        if len(w_name) != 0:
            # print("A %s" % w_name)
            self.wind_list.append(w_name)
        # if re.match(wildcard, w_name) is not None:
        # print("w_name:%s, wildcard:%s" % (w_name, wildcard))
        if w_name.find(wildcard) != -1:
            self._handle = hwnd

    def _child_window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        # print("call _child_window_enum_callback")
        w_name = str(win32gui.GetWindowText(hwnd))
        if len(w_name) != 0:
            self.wind_list.append(w_name)
            # print("C %s" % w_name)
        # if re.match(wildcard, w_name) is not None:
        if w_name.find(wildcard) != -1:
            self._child_handle = hwnd

    def print_window_list(self):
        for item in self.wind_list:
            sa_log("%s" % item)

    def find_child_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self.wind_list = []
        self._child_handle = None
        win32gui.EnumChildWindows(self._handle, self._child_window_enum_callback, wildcard)
        return self._child_handle

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        self.wind_list = []
        # print("AAAAAAAAAAAAAAAAAAAAAA")
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        # print("BBBBBBBBBBBBBBBBBBBBBB")
        return self._handle

    def close_window(self):
        if self._handle is not None:
            try:
                self.set_foreground()
                win32gui.PostMessage(self._handle, win32con.WM_CLOSE, 0, 0)
            except Exception as e:
                sa_log("Error: %s" % e)
                pass
        else:
            sa_log("Fail to close window")

    def set_foreground(self):
        """put the window in the foreground"""
        if self._handle is not None:

            if self._child_handle is not None:
                key_input.altInput()

            try:
                win32gui.SetForegroundWindow(self._handle)
                if self._child_handle is not None:
                    win32gui.SetForegroundWindow(self._child_handle)
            except Exception as e:
                sa_log("Error: %s" % e)
                pass
            return self._handle
        else:
            sa_log("Fail to find window")
            return None
