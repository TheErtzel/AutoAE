import win32api
import win32con
import os
import time
import glob
import threading
import pyautogui
from collections import Counter
from typing import Any, Union, List, Tuple, Dict

import utils.constants as consts
import utils.memory as memory
import utils.window as window
import utils.keyboard as keyboard
import utils.controller as controller


def send_text(msg: str) -> None:
    for hwnd in window.find_windows('Ashen Empires'):
        for c in msg:
            # loops through msg and sends each keystroke - ord() converts the given character to its ascii code
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
            time.sleep(0.05)


def send_key(msg: str) -> None:
    for hwnd in window.find_windows('Ashen Empires'):
        for k in msg:
            # loops through msg and sends each keystroke - ord() converts the given character to its ascii code
            keyboard.press(k, hwnd)
            time.sleep(0.05)


def bubble_sort(arr: List[str], ind: int = 6) -> List[str]:
    """Bubble sort arr based upon subelement ind (default of index 6)
       which is 7th element of sub-array since 0 based indexing"""
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n-i-1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if int(arr[j][ind]) > int(arr[j+1][ind]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def sort_tuple(tup: Tuple, sort_by: int = 1) -> List:
    return(sorted(tup, key=lambda x: x[sort_by]))


def shared_chars(s1: str, s2: str) -> int:
    return sum((Counter(s1) & Counter(s2)).values())


def filter(source: List, key: str) -> List:
    found = []
    result = []
    for element in source:
        unique = element[key]
        if not unique in found:
            found.append(unique)
            result.append(element)
    return result


def flatten(source: List, key: str) -> List:
    result = []
    for element in source:
        result.append(element[key])
    return result


def sort_by(source: List, key: str, reverse: bool = False) -> List:
    return sorted(source, key=lambda item: item[key], reverse=reverse)


def remove_from_array(source: List = [], element: Union[Any, None] = None) -> List:
    result = []
    if element in source:
        result = source.remove(element)
    else:
        for e in source:
            if e != element:
                result.append(e)
    return result


def get_last_logs(amount: int) -> str:
    path = f'{consts.AE_DIR}data\\User_Data\\*.log'
    files = glob.glob(path)
    lastestFile = max(files, key=os.path.getctime)
    lastLines = []
    with open(lastestFile, 'r') as file:
        lastLines = file.readlines()
    if amount > 0:
        return lastLines[-amount:]
    else:
        return lastLines


def get_last_channel_logs(channel: str, amount: int) -> List[str]:
    logs = get_last_logs(0)
    systemLogs = []
    for log in logs:
        if f'({channel})' in log:
            systemLogs.append(log.replace('\n', '').strip())
    if amount > 0:
        return systemLogs[-amount:]
    else:
        return systemLogs


def logs_have_message(chatLogs: List[str] = [], text: str = 'fizzled.', textOpposite: str = '') -> bool:
    textFound = False
    for log in chatLogs:
        checkline = str(log)
        if f'{text}' in checkline:
            textFound = True
        if textOpposite != '' and f'{textOpposite}' in checkline:
            textFound = False
    return textFound


def channel_logs_have_message(channel: str = 'System', text: str = 'fizzled.', amount: int = 5) -> List[str]:
    chatLogs = get_last_channel_logs(channel, amount)
    return [text for chatLog in chatLogs if text in chatLog]


def combat_logs_have_message(text: str = 'fizzled.') -> List[str]:
    chatLogs = get_last_channel_logs('Combat/Magic', 3)
    return [text for chatLog in chatLogs if text in chatLog]


def get_spell_result() -> int:
    chatLogs = get_last_channel_logs('Combat/Magic', 1)
    checkline = str(chatLogs[0])
    if 'You have cast' in checkline:
        return 1
    elif 'already has' in checkline or 'does not need' in checkline:
        return 2
    elif 'fizzled' in checkline:
        return 3
    elif 'is too far away' in checkline:
        return 4
    elif 'You cannot cast on that object' in checkline:
        return -1
    elif 'You cannot cast' in checkline and 'for another' in checkline:
        return 5
    else:
        return 0


def get_attack_result() -> int:
    chatLogs = get_last_channel_logs('Combat/Magic', 1)
    checkline = str(chatLogs[0])
    if 'You hit' in checkline:
        return 1
    elif 'is out of range' in checkline:
        return 2
    elif 'is too far away' in checkline:
        return 3
    else:
        return 0


def is_known_pet(name) -> bool:
    for pet in consts.PET_NAMES:
        if name == pet:
            return True
    return False


def get_distance_apart(sourceCoords: Tuple[Union[int, None]], targetCoords: Tuple[Union[int, None]]) -> tuple:
    xOffset = abs(targetCoords[0] - sourceCoords[0])
    yOffset = abs(targetCoords[1] - sourceCoords[1])

    if targetCoords[0] < sourceCoords[0]:
        xOffset = -abs(xOffset)
    if targetCoords[1] < sourceCoords[1]:
        yOffset = -abs(yOffset)

    return (xOffset, yOffset)


def click_location(x: int, y: int, offset: List[int] = [48, 55]) -> None:
    if x == None or y == None:
        return
    x += offset[0]
    y += offset[1]

    controller.move_mouse(x, y)
    time.sleep(0.250)
    controller.left_mouse_click(x, y)
    time.sleep(0.250)


def found_id_at_position(id: int, x: int, y: int) -> bool:
    controller.move_mouse(x, y, False)
    if memory.get_mouse_id() != 0:
        # if memory.get_mouse_id() == id:
        return True
    return False


def click_entity(id: int, baseX: int, baseY: int, offset: List[int] = [0, 0]) -> bool:
    if baseX == None or baseY == None:
        return False

    if found_id_at_position(id=id, x=baseX + offset[0], y=baseY + offset[1]):
        controller.left_mouse_click(
            x=baseX + offset[0], y=baseY + offset[1])
        time.sleep(0.250)
        return True

    return False


def click_self() -> None:
    selfCoords = get_own_screen_coords()
    if selfCoords[0] != None:
        controller.move_mouse(selfCoords[0], selfCoords[1] + 35, False)
        controller.left_mouse_click()


def replace_runes(bot, ids: List[int]) -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)

    pyautogui.keyDown('shift')
    time.sleep(0.250)

    for id in ids:
        if id == consts.Rune.BODY:
            bot.log(f'[Logic] Replacing Body Rune')
            pyautogui.press('f5')
        elif id == consts.Rune.MALENOX:
            bot.log(f'[Logic] Replacing Malenox Rune')
            pyautogui.press('f6')
        elif id == consts.Rune.AGON:
            bot.log(f'[Logic] Replacing Agon Rune')
            pyautogui.press('f7')
        elif id == consts.Rune.MALITH:
            bot.log(f'[Logic] Replacing Malith Rune')
            pyautogui.press('f8')
        elif id == consts.Rune.ULTHIEN:
            bot.log(f'[Logic] Replacing Ulthien Rune')
            pyautogui.press('f9')
        elif id == consts.Rune.SABAL:
            bot.log(f'[Logic] Replacing Sabal Rune')
            pyautogui.press('f10')
        elif id == consts.Rune.ISOS:
            bot.log(f'[Logic] Replacing Isos Rune')
            pyautogui.press('f11')
        elif id == consts.Rune.VELDAN:
            bot.log(f'[Logic] Replacing Veldan Rune')
            pyautogui.press('f12')

    time.sleep(0.250)
    pyautogui.keyUp('shift')
    time.sleep(0.250)


def check_runes(bot) -> None:
    rune_slots = memory.get_rune_slots()
    indexes = []

    if rune_slots > 0:
        Rune_types = memory.get_rune_types()
        Rune_charges = memory.get_rune_charges()
        for index in range(rune_slots - 1):
            charges = Rune_charges[index]
            time.sleep(0.100)
            if charges > 0 and charges <= 15:
                indexes.append(Rune_types[index])

    if len(indexes) > 0:
        replace_runes(bot, indexes)


def get_missing_health_percentage(value: int = 0, total: int = 0) -> int:
    if value == 0:
        return 100
    if total == 0:
        return 100
    return int((value/total) * 100)


def use_healing_potion() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f4')


def use_magical_weapon(bot) -> None:
    rune_slots = memory.get_rune_slots()

    if memory.get_hotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.set_hotbar(8)

    # Equip a magical weapon
    if rune_slots == 0:
        bot.log('[Logic] Switching to magical weapon')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('F1')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def use_body_rune(bot) -> None:
    rune_types = memory.get_rune_types()

    if memory.get_hotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.set_hotbar(8)

    # If we aren't using a body Rune, switch to one
    if len(rune_types) > 0 and rune_types[0] != consts.Rune.BODY:
        bot.log('[Logic] Switching Rune slot 0 to body')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('f5')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def use_rune(bot, rune_type: int) -> None:
    rune_types = memory.get_rune_types()

    if memory.get_hotbar() != 9:
        bot.log('[Logic] Switching to hotbar #9')
        memory.set_hotbar(9)

    # If we aren't using a mind Rune, switch to one
    if len(rune_types) > 0 and rune_types[0] != rune_type:
        if rune_type == consts.Rune.BODY:
            bot.log('[Logic] Switching Rune slot 0 to Body')
            pyautogui.press('f4')
        elif rune_type == consts.Rune.MIND:
            bot.log('[Logic] Switching Rune slot 0 to Mind')
            pyautogui.press('f5')
        elif rune_type == consts.Rune.NATURE:
            bot.log('[Logic] Switching Rune slot 0 to Nature')
            pyautogui.press('f6')
        elif rune_type == consts.Rune.SOUL:
            bot.log('[Logic] Switching Rune slot 0 to Soul')
            pyautogui.press('f7')
        time.sleep(0.250)


def use_none_magical_weapon(bot) -> None:
    RuneSlots = memory.get_rune_slots()

    if memory.get_hotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.set_hotbar(8)

    # Equip a non-magical weapon
    if RuneSlots > 0:
        bot.log('[Logic] Switching to non-magical weapon')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('F2')
        time.sleep(0.250)
        pyautogui.press('F3')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def select_spell(spell_id: int, hotbar_key: str) -> None:
    while memory.get_spell() != spell_id:
        pyautogui.press(hotbar_key)
        time.sleep(0.250)


def prepare_to_heal(bot) -> None:
    use_magical_weapon(bot)
    use_body_rune(bot)


def prepare_to_buff(bot) -> None:
    if memory.get_hotbar() != 2:
        bot.log('[Logic] Switching to hotbar #2')
        memory.set_hotbar(2)


def prepare_to_attack() -> None:
    if memory.get_spell() != 0:
        pyautogui.press('f2')
    # use_none_magical_weapon(bot)


def use_spell(bot, spell: int, spellType: int, coords: List[int], offsets: List[int]) -> Union[Any, None]:
    if not memory.get_spell() == spell:
        memory.set_spell(spell)
    if not memory.get_spell_state() == 1:
        memory.set_spell_state(1)
    if not memory.get_spell_type() == spellType:
        memory.set_spell_type(spellType)

    controller.move_mouse(coords[0] + offsets[0], coords[1] + [1], False)
    controller.left_mouse_click()
    spellResult = get_spell_result()
    if spellResult == 3:  # fizzled
        return use_spell(bot, spell, spellType, coords, offsets)
    elif spellResult != 2:
        time.sleep(3.0)
        check_runes(bot)


def use_healing_spell(bot) -> bool:
    prepare_to_heal(bot)
    select_spell(consts.Spell.SUPERIOR_HEAL, 'f2')

    bot.log('[Logic] Casting heal on self')
    click_self()
    spellResult = get_spell_result()
    if spellResult == 3:
        bot.log('[Logic] Superior Heal fizzled! Recasting...')
        return use_healing_spell(bot)
    elif spellResult != 2:
        time.sleep(consts.SpellTimer.SUPERIOR_HEAL)
        check_runes(bot)
        return True
    else:
        return False


def use_call_of_the_gods_spell(bot) -> bool:
    prepare_to_heal(bot)
    select_spell(consts.Spell.CALL_OF_THE_GODS, 'f6')

    bot.log('[Logic] Casting Call of the Gods on bot')
    click_self()
    spellResult = get_spell_result()
    if spellResult == 3:
        bot.log('[Logic] Call of the Gods fizzled! Recasting...')
        click_self()
    elif spellResult == 5:
        bot.log(
            '[Logic] Call of the Gods on cooldown! Switching to Superior Heal')
        return use_call_of_the_gods_spell(bot)
    elif spellResult != 2:
        time.sleep(consts.SpellTimer.CALL_OF_THE_GODS)
        check_runes(bot)
        return True
    else:
        return False


def use_stamina_potion() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f3')


def get_game_window_center() -> List[int]:
    screen = memory.get_screen()
    game_window = memory.get_game_window()
    game_width = screen[0] + game_window[0] + game_window[2]
    game_height = screen[1] + game_window[1] + game_window[3]
    return [int(game_width/2), int(game_height/2)]


def get_own_screen_coords() -> List[int]:
    tileWidth, tileHeight = consts.TILE_SIZE
    middleOfWindow = get_game_window_center()
    return [int(middleOfWindow[0] + (tileWidth / 2)), int(middleOfWindow[1] - (tileHeight / 2))]


def get_entity_screen_location(bot, entity: Dict[str, Any]) -> Dict[str, Any]:
    selfCoords = get_own_screen_coords()
    tileWidth, tileHeight = consts.TILE_SIZE
    xDif, yDif = entity['distance']
    tileOffset = 0
    xOffset = 0
    yOffset = 0

    if yDif < 0:
        yOffset = int(-abs(yDif * tileHeight) + (tileHeight / 1.5))
    else:
        yOffset = int(abs(yDif * tileHeight) - (tileHeight / 1.5))

    if yDif < 0:
        tileOffset = int(abs(yDif) * (tileWidth / 1.4) / 2)
    elif yDif >= 3:
        tileOffset = int(-abs(abs(yDif / 2) * (tileWidth / 1.55)))
    else:
        tileOffset = 0

    if xDif == 0:
        if tileOffset < 0:
            xOffset = int(-abs((xDif * tileWidth) + tileOffset))
        else:
            xOffset = int(abs((xDif * tileWidth) + tileOffset))
    elif xOffset < 0:
        xOffset = int(-abs((xDif * tileWidth) + tileOffset))
    else:
        xOffset = int(abs((xDif * tileWidth) + tileOffset))

    bot.log(f'[Logic] get_entity_screen_location xDif: {xDif}, yDif: {yDif}')
    bot.log(
        f'[Logic] get_entity_screen_location tileOffset: {tileOffset}, xOffset: {xOffset}, yOffset: {yOffset}')

    return {'coords': selfCoords, 'offsets': [xOffset, yOffset]}


def un_ignore_entity(bot, entity: Dict[str, Any]) -> None:
    if bot != None:
        bot.log(
            f'[Logic] Removed {entity["name"]} from temporary ignore list')
        bot.ignored_ids = remove_from_array(bot.ignored_ids, entity['id'])


def ignore_entity(bot, entity: Dict[str, Any]) -> None:
    def removeIgnored():
        un_ignore_entity(bot, entity)

    bot.log(f'[Logic] Added {entity["name"]} to temporary ignore list')
    bot.ignored_ids.append(entity['id'])
    bot.entities_on_screen = remove_from_array(bot.entities_on_screen, entity)
    # Remove entity id from ignore list after 10 seconds
    threading.Timer(interval=10, function=removeIgnored).start()


def buff_selected_entity(bot) -> None:
    entity: Union[Dict[str, Any], None] = bot.selected_entity
    if entity == None or bot.state != 1:
        return

    use_magical_weapon(bot)

    use_rune(bot, consts.Rune.MIND)
    bot.log(f'[Logic] Casting debuffs')
    prepare_to_buff(bot)
    if memory.get_spell() == 0:
        pyautogui.press('f2')
    location = get_entity_screen_location(bot, entity)
    for _ in range(3):
        if bot.state == 1:
            use_spell(bot, consts.Spell.ANARCHY, 5,
                      location['coords'], offsets=location['offsets'])

    if bot.state != 1:
        return

    buffs = [consts.Spell.RESPLENDENCE, consts.Spell.ALACRITY, consts.Spell.GRANDEUR, consts.Spell.GAZELLE, consts.Spell.AEGIS, consts.Spell.FAITH,
             consts.Spell.DARK_PRAYER, consts.Spell.BLESSING_OF_ARNA, consts.Spell.BULWARK_MIGHT, consts.Spell.HOLY_AURA, consts.Spell.FORTIFY]

    bot.log(f'[Logic] Casting buffs')
    prepare_to_buff(bot)

    if bot.state != 1:
        return

    location = get_entity_screen_location(bot, entity)
    for spell in range(len(buffs)-1):
        if bot.state == 1:
            use_spell(bot, spell, 5,
                      location['coords'], offsets=location['offsets'])

    bot.selected_entity = None


def heal_selected_entity(bot) -> None:
    bot.log(
        f'[Logic] heal_selected_entity: {bot.selected_entity}')
    entity: Union[Dict[str, Any], None] = bot.selected_entity
    if entity == None or bot.state != 1:
        return

    bot.log(
        f'[Logic] heal_selected_entity prepareing to heal')
    prepare_to_heal(bot)

    bot.log(
        f'[Logic] heal_selected_entity selecting spell')

    while memory.get_spell() != consts.Spell.SUPERIOR_HEAL and bot.state == 1:
        pyautogui.press('f2')
        time.sleep(0.250)

    if bot.state != 1:
        return

    bot.log(
        f'[Logic] Casting superior heal on [{entity["name"]}] ({entity["percentage"]}%)')

    location = get_entity_screen_location(bot, entity)
    entityFound = click_entity(entity['id'], location['coords'][0],
                               location['coords'][1], offset=location['offsets'])

    if not entityFound or bot.state != 1:
        bot.selected_entity = None
        return

    spellResult = get_spell_result()

    if spellResult == -1:
        bot.non_player_ids.append(entity['id'])
    elif spellResult == 3:
        bot.log('[Logic] Superior heal fizzled!')
        bot.worker_queue.add(name='heal_selected_entity', addToStart=True)
        return
    elif spellResult == 4 or spellResult == 5:
        ignore_entity(bot, entity)
        bot.selected_entity = None
    else:
        if spellResult != 2:
            time.sleep(consts.SpellTimer.SUPERIOR_HEAL)
            bot.selected_entity = None
            check_runes(bot)
        else:
            bot.selected_entity = None


def use_food() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f9')


def use_regeneration_totem() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f10')


def use_class_totem() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f11')


def use_werewolf_totem() -> None:
    if memory.get_hotbar() != 8:
        memory.set_hotbar(8)
    pyautogui.press('f12')


def target_new_enemy(bot) -> None:
    target = 0
    if memory.get_target_id() > 0 and get_attack_result() != 2:
        return

    bot.looking_for_target = True
    prepare_to_attack()

    bot.log('[Attacker] Looking for a new target...')
    tick = 0
    while tick < 30:
        if bot.state != 1:
            bot.looking_for_target = False
            break
        pyautogui.press('`')
        time.sleep(0.250)
        target = memory.get_target_id()
        if target > 0:
            time.sleep(0.250)
            if get_attack_result() != 2:
                bot.log(f'[Logic] Mew target found!')
                break
        pyautogui.press('~')
        time.sleep(0.250)
        target = memory.get_target_id()
        if target > 0:
            time.sleep(0.250)
            if get_attack_result() != 2:
                bot.log(f'[Logic] Mew target found!')
                break
        tick += 1
    if target == 0:
        bot.log(f'[Logic] Failed to find new target!')
    bot.looking_for_target = False


def get_entity_to_heal(bot) -> None:
    entities_on_screen = bot.entities_on_screen
    if len(entities_on_screen) == 0 or bot.state != 1:
        return

    bot.log(
        '[Logic] Checking for the entity on-screen in need of healing...')

    entity: Dict[str, Any] = entities_on_screen[0]
    partyAssistId = memory.get_party_assist_id()
    if partyAssistId > 0:
        for e in entities_on_screen:
            if partyAssistId == int(e['id']) and e['percentage'] <= 95:
                entity = e
                break

    # if entity['percentage'] <= 100:
    if entity['percentage'] <= 95:
        bot.log(
            f'[Logic] Entity to heal: {entity["name"]} ({entity["percentage"]}%)')
        bot.selected_entity = entity
        bot.worker_queue.add(name='heal_selected_entity', addToStart=True)
    else:
        bot.log(
            f'[Logic] Failed to find any entities in need of healing on the screen')


def get_entities_on_screen(bot) -> None:
    non_player_ids = bot.non_player_ids
    ignored_ids = bot.ignored_ids
    if bot.state != 1:
        return

    bot.log(f'[Logic] Updating entities on the screen...')
    selfLoc = memory.get_own_location()
    followerId = memory.get_follower_id()
    entities = []
    for offset in sorted(consts.SCREEN_ENTITY_OFFSETS):
        if bot.state != 1:
            break
        for i in range(1):
            if bot.state != 1:
                break

            hexCode = hex(offset + (i * 4))
            entity = memory.get_entity_data(hexCode)
            _id = entity['id']
            if _id == 0 or entity['name'] == '' or (entity['tag'] == '' and _id != followerId) or is_known_pet(entity['name']) or _id in non_player_ids or _id in ignored_ids:
                break

            distance = get_distance_apart(
                selfLoc, entity['coords'])
            if distance[0] <= 14 and distance[0] >= -13 and distance[1] <= 12 and distance[1] >= -12:
                entity['distance'] = distance
                entity['percentage'] = get_missing_health_percentage(
                    entity['hp'][0], entity['hp'][1])
                entities.append(entity)

    bot.entities_on_screen = sort_by(filter(entities, 'id'), 'percentage')
    if len(bot.entities_on_screen) > 0:
        bot.log(
            f'[Logic] Found {flatten(bot.entities_on_screen, "name")} on the screen...')
