import os
from enum import IntEnum
from typing import List, Tuple


directory: str = os.path.abspath(os.curdir)

ROOT_DIR: str = f'{directory}\\'
IMAGE_DIR: str = f'{ROOT_DIR}images\\'
PARTY_IMAGE_DIR: str = f'{IMAGE_DIR}party\\'
PARTY_MEMBERS_IMAGE_DIR: str = f'{PARTY_IMAGE_DIR}members\\'

AE_DIR = 'C:\\Program Files (x86)\\Pixel Mine\\Ashen Empires\\'
#AE_DIR: str = 'C:\\Sandbox\\james\\AE\\drive\\C\\Program Files (x86)\\Pixel Mine\\Ashen Empires\\'


GAME_REGION = {'top': 70, 'left': 10, 'width': 790, 'height': 530}

SELF_COORDS: Tuple[int] = (798, 437)
SELF_ONSCREEN_COORDS: Tuple[int] = (418, 320)
MIN_ONSCREEN_COORDS: Tuple[int] = (-10, -11)
MAX_ONSCREEN_COORDS: Tuple[int] = (8, 12)

TILE_SIZE: List[int] = [38, 26]


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
TIMER_BUFF: float = 3.0
TIMER_SUPERIOR_HEAL: float = 3.0

# On-Screen Entity Offsets
SCREEN_ROWS: List[List[int]] = [
    [  # Starts at X -14, Y -11, Ends at X +7, Y -11
        0x1C0,  0x88,  0x150,  0x18,  0xE0,  0x1A8,  0x138,  0x0,  0xC8,  0x190,
        0x58, 0x120,  0x1E8,  0xB0,  0x178,  0x140,  0x8,  0xD0,  0x198,  0xD0,  0x60
    ],
    [  # Starts at X -14, Y -10, Ends at X +7, Y -10
        0x30, 0xF8, 0xC0, 0x188, 0x50, 0x118, 0x1E0, 0xA8, 0x170, 0x38,
        0x100,  0x1C8, 0x90, 0x158, 0x20, 0xE8, 0x1B0, 0x78, 0x40, 0x108, 0x1D0
    ],
    [  # Starts at X -13, Y -9, Ends at X +7, Y -9
        0x68, 0x130, 0x1F8, 0x88, 0x150, 0x18, 0xE0, 0x1A8, 0x70
    ],
    [  # Starts at X -13, Y -10, Ends at X +8, Y -8
        0x1D8,  0xA0, 0x168
    ],
    [
        0x1A0, 0x1C0, 0x1F0, 0x1FC, 0x4C, 0x5C, 0x48, 0x40, 0x24, 0x28, 0x14, 0x10, 0xB8, 0xD8, 0x128, 0x160
    ]
]
