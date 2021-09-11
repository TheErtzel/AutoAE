import time
from win32api import GetCursorPos, SetCursorPos, mouse_event
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP


def getCursorPos():
    return GetCursorPos()


def smooth_move_mouse(from_x: int = 0, from_y: int = 0, to_x: int = 0, to_y: int = 0, speed: int = 0.2):
    steps = 40
    sleep_per_step = speed // steps
    x_delta = (to_x - from_x) / steps
    y_delta = (to_y - from_y) / steps
    for step in range(steps):
        new_x = x_delta * (step + 1) + from_x
        new_y = y_delta * (step + 1) + from_y
        SetCursorPos((int(new_x), int(new_y)))
        time.sleep(sleep_per_step)
    SetCursorPos((int(to_x), int(to_y)))


def move_mouse(x: int = 0, y: int = 0, smooth: bool = True):
    if smooth:
        curX, curY = getCursorPos()
        return smooth_move_mouse(curX, curY, x, y)
    else:
        SetCursorPos((int(x), int(y)))


def left_mouse_click(x: int = -1, y: int = -1):
    if x == -1 or y == -1:
        curX, curY = getCursorPos()
        if x == -1:
            x = curX
        if y == -1:
            y = curY
    mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(.1)
    mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def right_mouse_click(x: int = -1, y: int = -1):
    if x == -1 or y == -1:
        curX, curY = getCursorPos()
        if x == -1:
            x = curX
        if y == -1:
            y = curY
    mouse_event(MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(.1)
    mouse_event(MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
