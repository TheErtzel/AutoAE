import time
import pyautogui
import threading
from tkinter import *
from ReadWriteMemory import ReadWriteMemory

import utils.constants as consts
import utils.memory as memory
from utils.general import TakeScreenshot

def GetMissingHealthPercentage():
    health_total = memory.GetMaxHealth()
    health_value = memory.GetCurHealth()
    if health_value == 0 or health_total == 0: return 0
    return int(100 * float(health_value)/float(health_total))

def GetMilliseconds(value=None):
    _result = 0.250
    if value == None: return _result

    try:
        _result = value / 1000.0
    except Exception:
        _result = 0.250
    return  _result