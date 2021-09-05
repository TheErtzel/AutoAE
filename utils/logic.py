import win32api
import win32con
import win32gui
import os
import time
import glob
import pyautogui
from collections import Counter
from typing import Union, List, Tuple

import utils.constants as consts
import utils.memory as memory
import utils.window as window


def sendText(msg):
    for hwnd in window.find_windows('Ashen Empires'):
        for c in msg:
            # loops through msg and sends each keystroke - ord() converts the given character to its ascii code
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
            time.sleep(0.05)


def bubbleSort(arr: List[str], ind: int = 6):
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


def sort_Tuple(tup: Tuple, sortBy: int = 1):
    return(sorted(tup, key=lambda x: x[sortBy]))


def shared_chars(s1: str, s2: str):
    return sum((Counter(s1) & Counter(s2)).values())


def filter(source, key):
    found = []
    result = []
    for element in source:
        unique = element[key]
        if not unique in found:
            found.append(unique)
            result.append(element)
    return result


def flatten(source, key):
    result = []
    for element in source:
        result.append(element[key])
    return result


def sortBy(source, key, reverse=False):
    return sorted(source, key=lambda item: item[key], reverse=reverse)


def hexRange(start=0x0, stop=0x4, step=0x04):
    hexCodes = []
    while start < stop:
        hexCodes.append(start)
        start += step
    return hexCodes


def compare_strings(source: str, text: str):
    shared = shared_chars(source, text)
    out_of = len(source)
    if len(text) > out_of:
        out_of = len(text)
    percentage = (shared / out_of) * 100
    return [shared, percentage]


def getLastLogs(amount: int):
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


def getLastChannelLogs(channel: str, amount: int):
    logs = getLastLogs(0)
    systemLogs = []
    for log in logs:
        if f'({channel})' in log:
            systemLogs.append(log.replace('\n', '').strip())
    if amount > 0:
        return systemLogs[-amount:]
    else:
        return systemLogs


def checkLogsForMessage(chatLogs: List[str] = [], text: str = 'fizzled.', textOpposite: str = ''):
    # return [text for chatLog in chatLogs if text in chatLog]
    textFound = False
    for log in chatLogs:
        if f'({text})' in log:
            textFound = True
        elif textOpposite != '' and f'({textOpposite})' in log:
            textFound = False
    return textFound


def checkForChannelMessage(channel: str = 'System', text: str = 'fizzled.', amount: int = 5):
    chatLogs = getLastChannelLogs(channel, amount)
    return [text for chatLog in chatLogs if text in chatLog]


def checkForComatMessage(text: str = 'fizzled.'):
    chatLogs = getLastChannelLogs('Combat/Magic', 3)
    return [text for chatLog in chatLogs if text in chatLog]


def checkSpellResult():
    chatLogs = getLastChannelLogs('Combat/Magic', 1)
    checkline = str(chatLogs[0])
    if 'You have cast' in checkline:
        return 1
    elif 'already has' in checkline:
        return 2
    elif 'fizzled' in checkline:
        return 3
    elif 'is too far away' in checkline:
        return 4
    elif 'You cannot cast' in checkline:
        return 5
    else:
        return 0


def checkAttackResult():
    chatLogs = getLastChannelLogs('Combat/Magic', 1)
    checkline = str(chatLogs[0])
    if 'You hit' in checkline:
        return 1
    elif 'is out of range' in checkline:
        return 2
    elif 'is too far away' in checkline:
        return 3
    else:
        return 0


def getDistanceApart(sourceCoords: Tuple[Union[int, None]], targetCoords: Tuple[Union[int, None]]):
    xOffset = abs(targetCoords[0] - sourceCoords[0])
    yOffset = abs(targetCoords[1] - sourceCoords[1])

    if targetCoords[0] < sourceCoords[0]:
        xOffset = -abs(xOffset)
    if targetCoords[1] < sourceCoords[1]:
        yOffset = -abs(yOffset)

    return (xOffset, yOffset)


def clickLocation(bot, x: int, y: int, offset: List[int] = [48, 55]):
    if x == None or y == None:
        return
    x += offset[0]
    y += offset[1]

    bot.controller.move_mouse(x, y)
    time.sleep(0.250)
    bot.controller.left_mouse_click(x, y)
    time.sleep(0.250)


def foundIdAtPosition(bot, id: int, x: int, y: int):
    bot.controller.move_mouse(x, y, False)
    if memory.GetMouseId() == id:
        return True
    return False


def generateNpcRange(baseX: int, baseY: int):
    npcRange = [(baseX, baseY)]
    tileWidth = consts.TILE_SIZE[0]
    tileHeight = consts.TILE_SIZE[1]
    for x in range(5):
        for y in range(5):
            npcRange.append(
                (baseX - (x * tileWidth), baseY + (y * tileHeight)))
        for y in range(5):
            npcRange.append(
                (baseX + (x * tileWidth), baseY + (y * tileHeight)))
        for y in range(5):
            npcRange.append(
                (baseX - (x * tileWidth), baseY - (y * tileHeight)))
        for y in range(5):
            npcRange.append(
                (baseX + (x * tileWidth), baseY - (y * tileHeight)))
    return npcRange


def clickEntity(bot, id: int, baseX: int, baseY: int, offset: List[int] = [0, 0]):
    if baseX != None and baseY != None:
        foundID = False
        bot.log(
            f'clickEntity [1]: id: {id}, baseX: {baseX}, baseY: {baseY}, offset: {offset}')

        mouseX, mouseY = bot.controller.getCursorPos()
        foundID = foundIdAtPosition(
            bot, id, mouseX + offset[0], mouseY + offset[1])

        foundID = foundIdAtPosition(
            bot, id, baseX + offset[0], baseY + offset[1])

        if not foundID:
            npcRange = sort_Tuple(generateNpcRange(
                bot, baseX, baseY), 1)
            for nr in npcRange:
                if foundIdAtPosition(bot, id, nr[0] + offset[0], nr[1] + offset[1]):
                    foundID = True
                    break

        bot.log(f'clickEntity [6]: foundID: {foundID}')
        if foundID:
            bot.controller.left_mouse_click()
            time.sleep(0.250)


def clickSelf(bot):
    selfCoords = consts.SELF_COORDS
    if selfCoords[0] != None:
        clickLocation(bot, selfCoords[0], selfCoords[1], offset=[0, 0])


def replaceRunes(bot, ids: List[int]):
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)

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


def checkRunes(bot):
    Rune_slots = memory.GetRuneSlots()
    indexes = []

    if Rune_slots > 0:
        Rune_types = memory.GetRuneTypes()
        Rune_charges = memory.GetRuneCharges()
        for index in range(Rune_slots - 1):
            charges = Rune_charges[index]
            time.sleep(0.100)
            if charges > 0 and charges <= 15:
                indexes.append(Rune_types[index])

    if len(indexes) > 0:
        replaceRunes(bot, indexes)


def getMissingHealthPercentage(value, total):
    return int(value/total) * 100


def useHealingPotion():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f4')


def useMagicalWeapon(bot):
    RuneSlots = memory.GetRuneSlots()

    if memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.SetHotbar(8)

    # Equip a magical weapon
    if RuneSlots == 0:
        bot.log('[Logic] Switching to magical weapon')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('F1')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def useBodyRune(bot):
    RuneTypes = memory.GetRuneTypes()

    if memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.SetHotbar(8)

    # If we aren't using a body Rune, switch to one
    if len(RuneTypes) > 0 and RuneTypes[0] != consts.Rune.BODY:
        bot.log('[Logic] Switching Rune slot 0 to body')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('f5')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def useRune(bot, runeType: int):
    RuneTypes = memory.GetRuneTypes()

    if memory.GetHotbar() != 9:
        bot.log('[Logic] Switching to hotbar #9')
        memory.SetHotbar(9)

    # If we aren't using a mind Rune, switch to one
    if len(RuneTypes) > 0 and RuneTypes[0] != runeType:
        if runeType == consts.Rune.BODY:
            bot.log('[Logic] Switching Rune slot 0 to Body')
            pyautogui.press('f4')
        elif runeType == consts.Rune.MIND:
            bot.log('[Logic] Switching Rune slot 0 to Mind')
            pyautogui.press('f5')
        elif runeType == consts.Rune.NATURE:
            bot.log('[Logic] Switching Rune slot 0 to Nature')
            pyautogui.press('f6')
        elif runeType == consts.Rune.SOUL:
            bot.log('[Logic] Switching Rune slot 0 to Soul')
            pyautogui.press('f7')
        time.sleep(0.250)


def useNonMagicalWeapon(bot):
    RuneSlots = memory.GetRuneSlots()

    if memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        memory.SetHotbar(8)

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


def selectSpell(spell_id: int, hotbar_key: str):
    while memory.GetSpell() != spell_id:
        pyautogui.press(hotbar_key)
        time.sleep(0.250)


def prepareToHeal(bot):
    useMagicalWeapon(bot)
    useBodyRune(bot)


def prepareToBuff(bot):
    if memory.GetHotbar() != 2:
        bot.log('[Logic] Switching to hotbar #2')
        memory.SetHotbar(2)


def prepareToAttack():
    if memory.GetSpell() != 0:
        pyautogui.press('f2')
    # useNonMagicalWeapon(bot)


def useSpell(bot, spell: int, spellType: int, coords: List[int], offsets: List[int]):
    if not memory.GetSpell() == spell:
        memory.SetSpell(spell)
    if not memory.GetSpellState() == 1:
        memory.SetSpellState(1)
    if not memory.GetSpellType() == spellType:
        memory.SetSpellType(spellType)

    bot.controller.move_mouse(coords[0] + offsets[0], coords[1] + [1], False)
    bot.controller.left_mouse_click()
    spellResult = checkSpellResult()
    if spellResult() == 3:  # fizzled
        useSpell(bot, spell, spellType, coords, offsets)
    time.sleep(consts.TIMER_BUFF)
    checkRunes(bot)


def useHealingSpell(bot):
    prepareToHeal(bot)
    selectSpell(consts.Spell.SUPERIOR_HEAL, 'f2')

    bot.log('[Logic] Casting heal on self')
    clickSelf(bot)
    if checkSpellResult() == 3:
        bot.log('[Logic] Superior Heal fizzled! Recasting...')
        clickSelf(bot)
    time.sleep(consts.TIMER_SUPERIOR_HEAL)
    checkRunes(bot)


def useCallOfTheGodsSpell(bot):
    prepareToHeal(bot)
    selectSpell(consts.Spell.CALL_OF_THE_GODS, 'f6')

    bot.log('[Logic] Casting Call of the Gods on bot')
    clickSelf(bot)
    if checkSpellResult() == 3:
        bot.log('[Logic] Call of the Gods fizzled! Recasting...')
        clickSelf(bot)
    elif checkSpellResult() == 5:
        bot.log(
            '[Logic] Call of the Gods on cooldown! Switching to Superior Heal')
        return useHealingSpell(bot)
    time.sleep(consts.TIMER_SUPERIOR_HEAL)
    checkRunes(bot)


def useStaminaPotion():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f3')


def getEntityScreenLocation(bot, entity):
    selfCoords = consts.SELF_ONSCREEN_COORDS
    tileWidth, tileHeight = consts.TILE_SIZE
    xDif, yDif = entity['distance']

    xOffset = 0
    yOffset = 0
    if xDif < 0:
        xOffset = -abs(xDif * tileWidth)
    else:
        xOffset = abs(xDif * tileWidth)

    if yDif < 0:
        yOffset = -abs(yDif * tileHeight)
    else:
        yOffset = abs(yDif * tileHeight)

    bot.log(f'[Logic] getEntityScreenLocation xDif: {xDif}, yDif: {yDif}')
    bot.log(
        f'[Logic] getEntityScreenLocation xOffset: {xOffset}, yOffset: {yOffset}')

    return {'coords': selfCoords, 'offsets': [xOffset, yOffset]}


def buffEntity(bot, player):

    useMagicalWeapon(bot)

    useRune(bot, consts.Rune.MIND)
    bot.log(f'[Logic] Casting debuffs')
    prepareToBuff(bot)
    if memory.GetSpell() == 0:
        pyautogui.press('f2')

    location = getEntityScreenLocation(bot, player)
    for _ in range(3):
        useSpell(bot, consts.Spell.ANARCHY, 5,
                 location['coords'], offsets=location['offsets'])

    buffs = [consts.Spell.RESPLENDENCE, consts.Spell.ALACRITY, consts.Spell.GRANDEUR, consts.Spell.GAZELLE, consts.Spell.AEGIS, consts.Spell.FAITH,
             consts.Spell.DARK_PRAYER, consts.Spell.BLESSING_OF_ARNA, consts.Spell.BULWARK_MIGHT, consts.Spell.HOLY_AURA, consts.Spell.FORTIFY]

    bot.log(f'[Logic] Casting buffs')
    prepareToBuff(bot)

    location = getEntityScreenLocation(bot, player)
    for spell in range(len(buffs)-1):
        useSpell(bot, spell, 5,
                 location['coords'], offsets=location['offsets'])


def healEntity(bot, player):
    prepareToHeal(bot)

    while memory.GetSpell() != consts.Spell.SUPERIOR_HEAL:
        pyautogui.press('f2')
        time.sleep(0.250)

    bot.log(
        f'[Logic] Casting superior heal on player [{player["name"]}] ({player["percentage"]}%)')
    location = getEntityScreenLocation(bot, player)
    clickEntity(bot, player['id'], location['coords'][0],
                location['coords'][1], offset=location['offsets'])

    if checkSpellResult() == 3:
        bot.log('[Logic] Spell fizzled! Recasting...')
        location = getEntityScreenLocation(bot, player)
        clickEntity(bot, player['id'], location['coords'][0],
                    location['coords'][1], offset=location['offsets'])

    time.sleep(consts.TIMER_SUPERIOR_HEAL)
    checkRunes(bot)


def useFood():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f9')


def useRegenerationTotem():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f10')


def useClassTotem():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f11')


def useWerewolfTotem():
    if memory.GetHotbar() != 8:
        memory.SetHotbar(8)
    pyautogui.press('f12')


def getNewTarget(bot):
    target = 0
    if memory.GetTargetId() > 0 and checkAttackResult() != 2:
        return

    bot.looking_for_target = True
    prepareToAttack()

    bot.log('[Attacker] Looking for a new target...')
    tick = 0
    while tick < 30:
        if bot.state != 1:
            bot.looking_for_target = False
            break
        pyautogui.press('`')
        time.sleep(0.250)
        target = memory.GetTargetId()
        if target > 0:
            time.sleep(0.250)
            if checkAttackResult() != 2:
                bot.log(f'[Logic] Mew target found!')
                break
        pyautogui.press('~')
        time.sleep(0.250)
        target = memory.GetTargetId()
        if target > 0:
            time.sleep(0.250)
            if checkAttackResult() != 2:
                bot.log(f'[Logic] Mew target found!')
                break
        tick += 1
    if target == 0:
        bot.log(f'[Logic] Failed to find new target!')
    bot.looking_for_target = False


def getEntityToHeal(bot):
    entities_on_screen = bot.entities_on_screen
    if len(entities_on_screen) == 0:
        return

    memberToHeal = {'percentage': 100}
    bot.log(
        '[Logic] Checking for the entity on-screen with the lowest health percentage level...')
    for entity in entities_on_screen:
        if bot.state != 1:
            break

        percentage = entity['percentage']
        if percentage == None or percentage == 100:
            continue

        if percentage > memberToHeal['percentage']:
            memberToHeal = entity

    if 'name' in memberToHeal:
        entityName = memberToHeal["name"]
        bot.log(
            f'[Logic] Entity to heal: {entityName} ({memberToHeal["percentage"]}%)')
        healEntity(bot, memberToHeal)
    else:
        bot.log(
            f'[Logic] Failed to find any entities needing healing on the screen')


def getEntitiesOnScreen(bot):
    bot.log(f'[Logic] Updating entities on the screen...')

    selfLoc = memory.GetLocation()
    entities = []
    offset = consts.SCREEN_HEX[0]
    while offset < consts.SCREEN_HEX[1]:
        entity = memory.GetEntityData(offset)
        if entity['id'] != 0 and entity['name'] != '':
            distance = getDistanceApart(selfLoc, entity['coords'])
            if distance[0] <= 14 and distance[0] >= -13 and distance[1] <= 12 and distance[1] >= -12:
                curHP, maxHP = entity['hp']
                entity['distance'] = distance
                entity['percentage'] = getMissingHealthPercentage(curHP, maxHP)
                entities.append(entity)
        offset = offset + 4

    bot.entities_on_screen = filter(entities, 'id')
    bot.log(
        f'[Logic] Found {len(bot.entities_on_screen)} entities on the screen...')
