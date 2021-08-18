import os

directory = os.path.abspath(os.curdir)
KeyList = ['\t', '\n', '\r', ' ', '!', '"', '#', '_', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

_ROOT_DIR = f'{directory}\\'
_ImageDir = f'{_ROOT_DIR}images\\'
_PartyImageDir = f'{_ImageDir}party\\'
_PartyMembersImageDir = f'{_PartyImageDir}members\\'
_Image_TEMP_Dir = f'{_ROOT_DIR}images\\tmp\\'

_self_coords = [417, 340]
_playerOffsets = [0, 45]
_partyWindowOffset = [23, 3] # left, top
_partyMemberSize = [80, 10] # width, height
_partyMemberOffset = [10, 15] # top
_stamOffsets = [30, 1]
_healthOffsets = [50, 1]
_healthPotOffsets = [30, 1]
_partyHealthOffsets = [128, 0]

# Rune ID's
_rune_id_Body = 1453
_rune_id_Nature =  1455
_rune_id_Soul =  1454
_rune_id_Mind =  1452
_rune_id_Agon =  1461
_rune_id_Malenox =  1466
_rune_id_Malith =  1458
_rune_id_Ulthien =  1456
_rune_id_Kuthos =  1465
_rune_id_Veldan =  1457
_rune_id_Isos =  1464
_rune_id_Sabal =  1462
_rune_id_Adregard =  1463

# Spell ID's
_spell_none = -1
_spell_cog = 165
_spell_superior = 107
_spell_sustaining = 188
_spell_idol = 110
_spell_anarchy = 183
_spell_cerebral_thought = 124
_spell_resplendence = 185
_spell_bulwark = 179
_spell_holy_aura = 187
_spell_fortify = 18
_spell_alacrity = 27
_spell_grandeur = 181
_spell_gazelle = 190
_spell_aegis = 180
_spell_faith = 15
_spell_dark_prayer = 194
_spell_blessing = 113

# Spell Timers
_timer_spell_superior = 3.0