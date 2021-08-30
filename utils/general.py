from tkinter import *
from datetime import datetime


def GetTimestamp():
    dateTimeObj = datetime.now()
    timeObj = dateTimeObj.now().time()
    return timeObj.strftime("%H:%M:%S.%f")
