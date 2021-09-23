from ReadWriteMemory import ReadWriteMemory
from typing import Any, List, Tuple, Dict, Union

# Hex Codes             hex + 1000
_base = 0x400000  # 9/20
_base_self = 0x00353100  # 9/20
_base_entity = 0x003522D4  # 9/20
_base_follower = 0x00352F54  # 9/20
_base_gui = 0x003B3AB8  # 9/20
_base_hotbar = 0x00353158  # 9/22
_base_rune_type = 0x003B3B44  # 9/20
_base_rune_charge = 0x003B3B48  # 9/20
_base_spell = 0x003B3B48  # 9/20
_base_spell_type = 0x003B3A68  # 9/20
_base_game_window = 0x00353104  # 9/20

_z_offset = 0x2F0  # 8/24
_x_offset = 0x2F4  # 5/11
_y_offset = 0x2F8  # 5/11
_screen_width = 0x0048  # 8/12
_screen_height = 0x0044  # 8/12
_level_offset = 0x444  # 8/12
_max_health = 0x29C  # 8/11
_cur_health = 0x298  # 8/11
_stamina = 0x4A4  # 8/11
_stamina_regen = 0x57C  # 9/18
_armor = 0x2D0  # 8/12
_weight = 0x2A0  # 8/12
_message_offset = 0x003B1B50  # 9/17
_target_offset = 0x5F4  # 8/12
_follower_mode_offset = 0x48  # 8/12
_follower_id_offset = 0x0  # 10/09
_follower_hp_offset = 0x4C  # 8/12
_follower_hp_max_offset = 0x50  # 8/12
_can_move_offset = 0x678  # 8/14
_party_count_offset = 0x138  # 8/13
_hotbar_offset = 0x4  # 8/12
_poison_disease_offset = 0x580  # 8/13
_spell_offset = 0x10808  # 8/13
_spell_type_offset = 0x50  # 8/13
_spell_state_offset = 0x5F0  # 8/11
_rune_type_offset = 0x10818  # 8/15
_rune_charge_offset = 0x10840  # 8/13
_rune_slots_offset = 0x10810  # 8/13


class GameProcess():
    rmw = None
    process = None

    def __init__(self):
        try:
            self.rmw = ReadWriteMemory()
            #self.process = self.rmw.get_process_by_name("client.exe")
            self.process = self.rmw.get_process_by_id(55860)
        except:
            self.rmw = None
            self.process = None

    def __enter__(self):
        if self.process != None:
            self.process.open()
        return self.process

    def __exit__(self, type, value, traceback):
        if self.process != None:
            self.process.close()


def set_hotbar(number: int) -> bool:
    result: bool = False
    if number == 0:
        towrite = 48
    elif number == 1:
        towrite = 49
    elif number == 2:
        towrite = 50
    elif number == 3:
        towrite = 51
    elif number == 4:
        towrite = 52
    elif number == 5:
        towrite = 53
    elif number == 6:
        towrite = 54
    elif number == 7:
        towrite = 55
    elif number == 8:
        towrite = 56
    elif number == 9:
        towrite = 57
    else:
        towrite = 57
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_hotbar, offsets=[_hotbar_offset])
            result = process.write(point, towrite)
    return result


def set_spell(number: int) -> bool:
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_spell, offsets=[_spell_offset])
            result = process.write(point, number)
    return result


def set_spell_state(number: int) -> bool:
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_spell_state_offset])
            result = process.write(point, number)
    return result


def set_spell_type(number: int) -> bool:
    # [number] 0 = none, 2 = combat, 3 = heal, 5 = buff?,  8 = res?, 16 = AoE combat, 17 = AoE heal
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_spell_type, offsets=[_spell_type_offset])
            result = process.write(point, number)
    return result


def set_rune_types(rune_types: List[int]) -> List[bool]:
    result_list: List[bool] = []
    typeOffset = _rune_type_offset
    with GameProcess() as process:
        if process != None:
            for i in range(len(rune_types)):
                point = process.get_pointer(
                    _base + _base_spell, offsets=[typeOffset])
                result = process.write(point, rune_types[i])
                result_list.append(result)
                typeOffset = typeOffset + 4
    return result_list


def set_rune_charges(rune_charges: List[int]) -> List[bool]:
    result_list: List[bool] = []
    charge_offset = _rune_charge_offset
    with GameProcess() as process:
        if process != None:
            for i in range(len(rune_charges)):
                point = process.get_pointer(
                    _base + _base_spell, offsets=[charge_offset])
                result = process.write(point, rune_charges[i])
                result_list.append(result)
                charge_offset = charge_offset + 4
    return result_list


def get_program_width() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_screen_width])
            result = process.read(point)
    return result


def get_program_height() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_screen_height])
            result = process.read(point)
    return result


def get_own_y() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_entity, offsets=[_y_offset])
            result = process.read(point)
    return result


def get_own_x() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_entity, offsets=[_x_offset])
            result = process.read(point)
    return result


def get_own_z() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_entity, offsets=[_z_offset])
            result = process.read(point)
    return result


def get_own_location() -> Tuple:
    result: tuple = (None, None, None)
    with GameProcess() as process:
        if process != None:
            pointX = process.get_pointer(
                _base + _base_entity, offsets=[_x_offset])
            resultX = process.read(pointX)
            pointY = process.get_pointer(
                _base + _base_entity, offsets=[_y_offset])
            resultY = process.read(pointY)
            pointZ = process.get_pointer(
                _base + _base_entity, offsets=[_z_offset])
            resultZ = process.read(pointZ)
            result = (resultX, resultY, resultZ)
    return result


def get_mouse_x() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0680])
            result = process.read(point)
    return result


def get_mouse_y() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0684])
            result = process.read(point)
    return result


def get_mouse_state() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0678])
            result = process.read(point)
    return result


def get_mouse_id() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x05F8])
            result = process.read(point)
    return result


def set_mouse_x(position=0) -> bool:
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0680])
            result = process.write(point, position)
    return result


def set_mouse_y(position=0) -> bool:
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0684])
            result = process.write(point, position)
    return result


def set_mouse_state(state=0) -> bool:
    result: bool = False
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0678])
            result = process.write(point, state)
    return result


def get_screen() -> Tuple:
    result: tuple = (None, None, None, None)
    with GameProcess() as process:
        if process != None:
            pointLeft = process.get_pointer(_base + _base_gui, offsets=[0x30])
            resultLeft = process.read(pointLeft)
            pointTop = process.get_pointer(_base + _base_gui, offsets=[0x40])
            resultTop = process.read(pointTop)
            pointRight = process.get_pointer(
                _base + _base_gui, offsets=[0x44])
            resultRight = process.read(pointRight)
            pointBottom = process.get_pointer(
                _base + _base_gui, offsets=[0x48])
            resultBottom = process.read(pointBottom)
            result = (resultLeft, resultTop, resultRight, resultBottom)
    return result


def get_game_window() -> Tuple:
    result: tuple = (None, None, None, None)
    with GameProcess() as process:
        if process != None:
            pointLeft = process.get_pointer(
                _base + _base_game_window, offsets=[0x3C])
            resultLeft = process.read(pointLeft)
            pointTop = process.get_pointer(
                _base + _base_game_window, offsets=[0x40])
            resultTop = process.read(pointTop)
            pointRight = process.get_pointer(
                _base + _base_game_window, offsets=[0x44])
            resultRight = process.read(pointRight)
            pointBottom = process.get_pointer(
                _base + _base_game_window, offsets=[0x48])
            resultBottom = process.read(pointBottom)
            result = (resultLeft, resultTop, resultRight, resultBottom)
    return result


def get_hotbar() -> int:
    result: int = -1
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_hotbar, offsets=[_hotbar_offset])
            id = process.read(point)
            if id == 48:
                result = 0
            elif id == 49:
                result = 1
            elif id == 50:
                result = 2
            elif id == 51:
                result = 3
            elif id == 52:
                result = 4
            elif id == 53:
                result = 5
            elif id == 54:
                result = 6
            elif id == 55:
                result = 7
            elif id == 56:
                result = 8
            elif id == 57:
                result = 9
    return result


def get_spell() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_spell, offsets=[_spell_offset])
            result = process.read(point)
            if result == 4294967295:
                result = 0
    return result


def get_spell_state() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_spell_state_offset])
            result = process.read(point)
    return result


def get_spell_type() -> int:
    # 0 = none, 2 = combat, 3 = heal, 5 = buff?,  8 = res?, 16 = AoE combat, 17 = AoE heal
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_spell_type, offsets=[_spell_type_offset])
            result = process.read(point)
    return result


def get_rune_types() -> List[int]:
    rune_list: List[int] = []
    typeOffset = _rune_type_offset
    with GameProcess() as process:
        if process != None:
            for _ in range(9):
                point = process.get_pointer(
                    _base + _base_spell, offsets=[typeOffset])
                result = process.read(point)
                rune_list.append(result)
                typeOffset = typeOffset + 4
    return rune_list


def get_rune_charges() -> List[int]:
    charge_list: List[int] = []
    charge_offset = _rune_charge_offset
    with GameProcess() as process:
        if process != None:
            for _ in range(9):
                point = process.get_pointer(
                    _base + _base_spell, offsets=[charge_offset])
                result = process.read(point)
                charge_list.append(result)
                charge_offset = charge_offset + 4
    return charge_list


def get_rune_slots() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_spell, offsets=[_rune_slots_offset])
            result = process.read(point)
    return result


def can_move() -> int:
    # returns 1 if you can move, 0 if not.
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_can_move_offset])
            result = process.read(point)
    return result == 1


def get_level() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_level_offset])
            result = process.read(point)
    return result


def get_poison_or_disease() -> int:
    # returns 4294967295 or -1 for none, 256 for disease, 1 for poison
    result: int = -1
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_poison_disease_offset])
            result = process.read(point)
            if result == 4294967295:
                result = 0
    return result


def get_armor() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_armor])
            result = process.read(point)
    return result


def get_weight() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_weight])
            num = process.read(point)
            result = int(num)
            if num > 0:
                # convert to a string to remove the last 2 numbers then convert back to an int
                result = int(str(num)[:-2])
    return result


def get_stamina() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_stamina])
            result = process.read(point)
    return result


def get_stamina_regen() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_stamina_regen])
            result = process.read(point)
    return result


def get_health() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_cur_health])
            result = process.read(point)
    return result


def get_health_max() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_self, offsets=[_max_health])
            result = process.read(point)
    return result


def get_party_count() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_gui, offsets=[_party_count_offset])
            result = process.read(point)
    return result


def get_party_assist_id() -> int:
    result: int = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(
                _base + _base_gui, offsets=[0x24, 0x6A8])
            result = process.read(point)
            if result == 4294967295:
                result = 0
    return result


def get_party_member_ids() -> List[int]:
    partyCount: int = get_party_count()
    data: list[int] = []
    with GameProcess() as process:
        if process != None:
            for i in range(partyCount):
                offsets = [0]
                for __ in range(i):
                    offsets.append(0)
                pointerId = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x08])
                resultId = process.read(pointerId)
                data.append(resultId)
    return data


def get_party_member_locations() -> List[tuple]:
    partyCount: int = get_party_count()
    locations: list[tuple] = []
    with GameProcess() as process:
        if process != None:
            for i in range(partyCount):
                offsets = [0]
                for _ in range(i):
                    offsets.append(0)
                pointX = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x44])
                resultX = process.read(pointX)
                pointY = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x48])
                resultY = process.read(pointY)
                pointZ = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x4C])
                resultZ = process.read(pointZ)
                locations.append((resultX, resultY, resultZ))
    return locations


def get_party_member_names() -> List[str]:
    partyCount: int = get_party_count()
    names: list[str] = []
    with GameProcess() as process:
        if process != None:
            for i in range(partyCount):
                offsets = [0]
                for _ in range(i):
                    offsets.append(0)
                pointer = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x000C])
                result = process.readString(pointer, 20)
                names.append(result)
    return names


def get_party_member_data() -> List:
    partyCount: int = get_party_count()
    data: list = []
    with GameProcess() as process:
        if process != None:
            for i in range(partyCount):
                offsets = [0]
                for _ in range(i):
                    offsets.append(0)
                pointerId = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x08])
                resultId = process.read(pointerId)
                pointerName = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x0C])
                resultName = process.readString(pointerName, 20)
                pointX = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x44])
                resultX = process.read(pointX)
                pointY = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x48])
                resultY = process.read(pointY)
                pointZ = process.get_pointer(
                    _base + _base_gui, offsets=[0x134] + offsets + [0x4C])
                resultZ = process.read(pointZ)
                data.append(
                    {'index': x, 'id': resultId, 'name': resultName, 'coords': (resultX, resultY, resultZ)})
    return data


def get_party_members_location(index: int) -> Tuple:
    offsets: List[int] = [0]
    for i in range(index):
        offsets.append(0)
    result: tuple = (None, None, None)
    with GameProcess() as process:
        if process != None:
            pointX = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x44])
            resultX = process.read(pointX)
            pointY = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x48])
            resultY = process.read(pointY)
            pointZ = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x4C])
            resultZ = process.read(pointZ)
            result = (resultX, resultY, resultZ)
    return result


def get_party_members_name(index: int) -> str:
    offsets: List[int] = [0]
    for i in range(index):
        offsets.append(0)
    result = None
    with GameProcess() as process:
        if process != None:
            pointer = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x000C])
            result = process.readString(pointer, 20)
    return result


def get_party_members_data(index: int) -> Dict[str, Union[int, str, Tuple]]:
    offsets: List[int] = [0]
    for i in range(index):
        offsets.append(0)
    result = {'index': -1, 'id': None,
              'name': None, 'coords': (None, None, None)}
    with GameProcess() as process:
        if process != None:
            pointerId = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x08])
            resultId = process.read(pointerId)
            pointerName = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x000C])
            resultName = process.readString(pointerName, 20)
            pointX = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x44])
            resultX = process.read(pointX)
            pointY = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x48])
            resultY = process.read(pointY)
            pointZ = process.get_pointer(
                _base + _base_gui, offsets=[0x134] + offsets + [0x4C])
            resultZ = process.read(pointZ)
            result = {'index': index, 'id': resultId, 'name': resultName,
                      'coords': (resultX, resultY, resultZ)}
    return result


def get_entity_data(offset: bytes) -> Dict[str, Union[int, str, Tuple]]:
    result = {'id': 0, 'name': '', 'tag': '',
              'coords': (0, 0), 'hp': (0, 0)}
    with GameProcess() as process:
        if process != None:
            pointerName = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x10C])
            resultName = process.readString(pointerName, 20)
            if resultName == None or len(resultName) == 0:
                return result

            pointerId = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x4])
            resultId = process.read(pointerId)
            pointerGuildTag = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x13C])
            resultGuildTag = process.readString(pointerGuildTag, 20)
            pointerX = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0xC])
            resultX = process.read(pointerX)
            pointerY = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x10])
            resultY = process.read(pointerY)
            pointerHP = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x18])
            resultHP = process.read(pointerHP)
            pointerMaxHP = process.get_pointer(
                _base + _base_entity, offsets=[0x210, offset, 0xC, 0x44, 0x1C])
            resultMaxHP = process.read(pointerMaxHP)
            if resultId > 0:
                result = {'id': resultId, 'name': resultName, 'tag': resultGuildTag, 'coords': (
                    resultX, resultY), 'hp': (resultHP, resultMaxHP)}
    return result


def get_target_id() -> int:
    # returns 0 if no target is selected, and the target id if it is.
    result: int = 0
    with GameProcess() as process:
        point = process.get_pointer(
            _base + _base_self, offsets=[_target_offset])
        result = process.read(point)
        if result == 4294967295:
            result = 0
    return result


def get_followers_id() -> List[int]:
    result: List[int] = [0, 0, 0]
    with GameProcess() as process:
        if process != None:
            offset = _follower_id_offset
            for i in range(2):
                offset = offset + (i * 0x58)
                point = process.get_pointer(
                    _base + _base_follower, offsets=[offset])
                result_id = process.read(point)
                if result_id == 4294967295:
                    result_id = 0
                result[i] = result_id
    return result


def get_followers_state() -> List[int]:
    # 0 = None, 11 = Follow, 12 = Stay, 13 = Protect, 15 = Guard, 16 = Attack, 17 = Inv, 18 = Flee, 19 = Assist
    result: List[int] = [0, 0, 0]
    with GameProcess() as process:
        if process != None:
            offset = _follower_mode_offset
            for i in range(2):
                offset = offset + (i * 0x58)
                point = process.get_pointer(
                    _base + _base_follower, offsets=[offset])
                result[i] = process.read(point)
    return result


def set_followers_state(state: int = 0) -> List[bool]:
    # [state] 0 = None, 11 = Follow, 12 = Stay, 13 = Protect, 15 = Guard, 16 = Attack, 17 = Inv, 18 = Flee, 19 = Assist
    result: List[bool] = [False, False, False]
    with GameProcess() as process:
        if process != None:
            offset = _follower_mode_offset
            for i in range(2):
                offset = offset + (i * 0x58)
                point = process.get_pointer(
                    _base + _base_follower, offsets=[offset])
                result[i] = process.write(point, state)
    return result


def set_follower_state(index: int = 0, state: int = 0) -> bool:
    # [state] 0 = None, 11 = Follow, 12 = Stay, 13 = Protect, 15 = Guard, 16 = Attack, 17 = Inv, 18 = Flee, 19 = Assist
    result: bool = False
    with GameProcess() as process:
        if process != None:
            offset = _follower_mode_offset + (index * 0x58)
            point = process.get_pointer(
                _base + _base_follower, offsets=[offset])
            result = process.write(point, state)
    return result


def get_followers_health() -> List[int]:
    result: List[int] = [0, 0, 0]
    with GameProcess() as process:
        if process != None:
            offset = _follower_hp_offset
            for i in range(2):
                offset = offset + (i * 0x58)
                point = process.get_pointer(
                    _base + _base_follower, offsets=[offset])
                result[i] = process.read(point)
    return result


def get_followers_health_max() -> List[int]:
    result: List[int] = [0, 0, 0]
    with GameProcess() as process:
        if process != None:
            offset = _follower_hp_max_offset
            for i in range(2):
                offset = offset + (i * 0x58)
                point = process.get_pointer(
                    _base + _base_follower, offsets=[offset])
                result[i] = process.read(point)
    return result


def get_system_message() -> str:
    result: str = ''
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _message_offset)
            result = process.readString(point, 500)
    return result


def get_guild_message() -> str:
    result: str = ''
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _message_offset)
            result = process.readString(point, 500)
    return result
