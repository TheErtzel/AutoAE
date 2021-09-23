from enum import IntEnum, EnumMeta
from typing import List

AE_DIR: str = 'C:\\Program Files (x86)\\Pixel Mine\\Ashen Empires\\'
#AE_DIR: str = 'C:\\Sandbox\\james\\AE\\drive\\C\\Program Files (x86)\\Pixel Mine\\Ashen Empires\\'

PET_NAMES: List[str] = ['Bonecrusher', 'Marrowsucker', 'Deceiver']

TILE_SIZE: List[int] = [38, 26]

# On-Screen Entity Offsets
SCREEN_ENTITY_OFFSETS: List[int] = [
    0x4, 0x1C0,  0x34, 0x88,  0x150,  0x18,  0xE0,  0x1A8,  0x138,  0x0,  0xC8,  0x190, 0x134, 0x148,  0x58, 0x120,  0x1E8,  0xB0,  0x178,
    0x140,  0x8,  0xD0,  0x198,  0x60, 0x30, 0xF8, 0xC0, 0x188, 0x50, 0x118, 0x1E0, 0xA8, 0x170, 0x38, 0x100, 0x1C8, 0x90, 0x158,
    0x20, 0xE8, 0x1B0, 0x78, 0x40, 0x108, 0x1D0, 0x1D4, 0x68, 0x130, 0x1F8, 0x88, 0x18, 0xE0, 0x1A8, 0x70, 0x1D8,  0xA0, 0x168, 0x50,
    0x98, 0x110, 0x1B8, 0x1A0, 0x1C0, 0x1F0, 0x1FC, 0x4C, 0x5C, 0x48, 0x40, 0x24, 0x28, 0x14, 0x10, 0xB8, 0xD8, 0x128, 0x160, 0x80
]
SCREEN_ENTITY_LIMITS: List[int] = [0x0, 0x200]


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
    BLESSING_OF_ARNA = 110
    ANARCHY = 183
    CEREBRAL_THOUGHT = 124
    RESPLENDENCE = 185
    BULWARK_MIGHT = 179
    HOLY_AURA = 187
    FORTIFY = 18
    ALACRITY = 27
    GRANDEUR = 181
    GAZELLE = 190
    AEGIS_OF_ARNA = 180
    FAITH = 15
    DARK_PRAYER = 194
    BLESSING_OF_MALAX = 113


class Spell_Bar(EnumMeta):
    """Spell Hotbar keys"""
    NONE = ''
    CALL_OF_THE_GODS = 'f6'
    SUPERIOR_HEAL = 'f2'
    SUSTAINING_HEAL = 'f8'
    BLESSING_OF_ARNA = 'f9'
    ANARCHY = 'f2'
    CEREBRAL_THOUGHT = 'f2'
    RESPLENDENCE = 'f3'
    BULWARK_MIGHT = 'f10'
    HOLY_AURA = 'f11'
    FORTIFY = 'f12'
    ALACRITY = 'f4'
    GRANDEUR = 'f5'
    GAZELLE = 'f5'
    AEGIS_OF_ARNA = 'f6'
    FAITH = 'F7'
    DARK_PRAYER = 'F8'
    BLESSING_OF_MALAX = 'F9'


class SpellTimer(IntEnum):
    """Spell Timerss"""
    NONE = 0
    CALL_OF_THE_GODS = 3
    SUPERIOR_HEAL = 3
    SUSTAINING_HEAL = 3
    BLESSING_OF_ARNA = 3
    ANARCHY = 3
    CEREBRAL_THOUGHT = 3
    RESPLENDENCE = 3
    BULWARK_MIGHT = 3
    HOLY_AURA = 3
    FORTIFY = 3
    ALACRITY = 3
    GRANDEUR = 3
    GAZELLE = 3
    AEGIS_OF_ARNA = 3
    FAITH = 3
    DARK_PRAYER = 3
    BLESSING_OF_MALAX = 3
