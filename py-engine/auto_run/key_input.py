# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : key_input.py
  Release  : 1
  Date     : 2018-09-22
 
  Description : Windows Input module
  
  Notes :
  ===================
  History
  ===================
  2018/09/22  created by Kim, Seongrae

'''
# common package import
import time

from common import *

# fishing module package import
# import win32api, win32con
from pyautogui import press, typewrite, hotkey
from pynput.mouse import Button, Controller
# import pyperclip
import win32clipboard


# python -m pip install pyperclip

def keyInput(string):
    press(string)


def tabInput():
    hotkey('tab')


def altInput():
    hotkey('alt')


def press_paste(text_to_paste):
    for ch in text_to_paste:
        win32clipboard.OpenClipboard()
        win32clipboard.SetClipboardText("%s" % (ch))
        win32clipboard.CloseClipboard()
        time.sleep(0.05)
        hotkey('ctrl', 'v')
        time.sleep(0.05)
    time.sleep(1.0)


def mouseInput(width, height, x, y, hot_key):
    mouse = Controller()

    move_unit = 32
    n_x_search = int(width / move_unit)
    n_y_search = int(height / move_unit)

    # mouse.move(x, y)
    mouse.position = (y, x)
    for i in range(n_y_search):
        for j in range(n_x_search):
            yy = y + (i * move_unit)
            xx = x + (j * move_unit)
            # mv_y = move_unit * (1 if i%2 == 0 else -1)
            # mouse.moive(mv_y, 0)
            mouse.position = (xx, yy)
            keyInput(hot_key)
        # mouse.move = (0, move_unit)
