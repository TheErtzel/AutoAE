import os

directory = os.path.abspath(os.curdir)
KeyList = ['\t', '\n', '\r', ' ', '!', '"', '#', '_', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
           'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

ROOT_DIR = f'{directory}\\'
ImageDir = f'{ROOT_DIR}images\\'
PartyImageDir = f'{ImageDir}party\\'
PartyMembersImageDir = f'{PartyImageDir}members\\'
Image_TEMP_Dir = f'{ROOT_DIR}images\\tmp\\'

self_coords = [417, 340]
playerOffsets = [0, 45]
partyWindowOffset = [23, 3]  # left, top
partyMemberSize = [80, 10]  # width, height
partyMemberOffset = [10, 15]  # top
stamOffsets = [30, 1]
healthOffsets = [50, 1]
healthPotOffsets = [30, 1]
partyHealthOffsets = [128, 0]
game_region = {'top': 70, 'left': 10, 'width': 790, 'height': 530}

# Rune ID's
rune_id_Body = 1453
rune_id_Nature = 1455
rune_id_Soul = 1454
rune_id_Mind = 1452
rune_id_Agon = 1461
rune_id_Malenox = 1466
rune_id_Malith = 1458
rune_id_Ulthien = 1456
rune_id_Kuthos = 1465
rune_id_Veldan = 1457
rune_id_Isos = 1464
rune_id_Sabal = 1462
rune_id_Adregard = 1463

# Spell ID's
spell_none = -1
spell_cog = 165
spell_superior = 107
spell_sustaining = 188
spell_idol = 110
spell_anarchy = 183
spell_cerebral_thought = 124
spell_resplendence = 185
spell_bulwark = 179
spell_holy_aura = 187
spell_fortify = 18
spell_alacrity = 27
spell_grandeur = 181
spell_gazelle = 190
spell_aegis = 180
spell_faith = 15
spell_dark_prayer = 194
spell_blessing = 113

# Spell Timers
timer_spell_superior = 3.0
