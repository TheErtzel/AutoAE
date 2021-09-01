import os
from enum import IntEnum

directory = os.path.abspath(os.curdir)

ROOT_DIR = f'{directory}\\'
IMAGE_DIR = f'{ROOT_DIR}images\\'
PARTY_IMAGE_DIR = f'{IMAGE_DIR}party\\'
PARTY_MEMBERS_IMAGE_DIR = f'{PARTY_IMAGE_DIR}members\\'

GAME_REGION = {'top': 70, 'left': 10, 'width': 790, 'height': 530}

SELF_COORDS = (798, 437)
SELF_ONSCREEN_COORDS = (418, 320)
MIN_ONSCREEN_COORDS = (-10, -11)
MAX_ONSCREEN_COORDS = (8, 12)

TILE_SIZE = 34


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
