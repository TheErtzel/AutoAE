import time
import win32api
import win32con
from pynput.mouse import Button, Controller as MouseController


class Controller:
    def __init__(self):
        self.mouse = MouseController()

    def getCursorPos(self):
        return win32api.GetCursorPos()

    def mouse_set(self, x, y):
        def set_mouse_position(x, y):
            win32api.SetCursorPos((int(x), int(y)))

        return set_mouse_position(x, y)

    def move_mouse(self, x, y):
        def set_mouse_position(x, y):
            win32api.SetCursorPos((int(x), int(y)))

        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=0.2):
            steps = 40
            sleep_per_step = speed // steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)

        return smooth_move_mouse(self.getCursorPos()[0], self.getCursorPos()[1], x, y)

    def left_mouse_click(self, x=None, y=None):
        if x == None or y == None:
            curX, curY = self.getCursorPos()
            if x == None:
                x = curX
            if y == None:
                y = curY
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def right_mouse_click(self, x=None, y=None):
        if x == None or y == None:
            curX, curY = self.getCursorPos()
            if x == None:
                x = curX
            if y == None:
                y = curY
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
