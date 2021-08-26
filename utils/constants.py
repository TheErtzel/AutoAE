import os
from enum import IntEnum

directory = os.path.abspath(os.curdir)
KeyList = ['\t', '\n', '\r', ' ', '!', '"', '#', '_', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
           'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

ROOT_DIR = f'{directory}\\'
IMAGE_DIR = f'{ROOT_DIR}images\\'
PARTY_IMAGE_DIR = f'{IMAGE_DIR}party\\'
PARTY_MEMBERS_IMAGE_DIR = f'{PARTY_IMAGE_DIR}members\\'

GAME_REGION = {'top': 70, 'left': 10, 'width': 790, 'height': 530}

SELF_ONSCREEN_COORDS = (418, 320)
MIN_ONSCREEN_COORDS = (-10, -11)
MAX_ONSCREEN_COORDS = (8, 12)


class Rune(IntEnum):
    """Rune IDs"""
    BODY = 1453
    NATURE = 1455
    SOUL = 1454
    MIND = 1452
    AGON = 1461
    MALENOX = 1466
    MALITH = 1458
    ULTHIEN = 1456
    KUTHOS = 1465
    VELDAN = 1457
    ISOS = 1464
    SABAL = 1462
    ADREGARD = 1463


class Spell(IntEnum):
    """Spell IDs"""
    NONE = -1
    CALL_OF_THE_GODS = 165
    SUPERIOR_HEAL = 107
    SUSTAINING_HEAL = 188
    IDOL_OF_ARNA = 110
    ANARCHY = 183
    CEREBRAL_THOUGHT = 124
    RESPLENDENCE = 185
    BULWARK_MIGHT = 179
    HOLY_AURA = 187
    FORTIFY = 18
    ALACRITY = 27
    GRANDEUR = 181
    GAZELLE = 190
    AEGIS = 180
    FAITH = 15
    DARK_PRAYER = 194
    BLESSING_OF_ARNA = 113


# Spell Timers
TIMER_SUPERIOR_HEAL = 3.0
