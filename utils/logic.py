import random
import os
import time
import glob
import traceback
import pyautogui
import numpy as np
from PIL import ImageGrab
from collections import Counter

from tkinter import *


def bubbleSort(arr, ind=6):
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


def sort_Tuple(tup, sortBy=1):
    return(sorted(tup, key=lambda x: x[sortBy]))


def shared_chars(s1, s2):
    return sum((Counter(s1) & Counter(s2)).values())


def compare_strings(source, text):
    shared = shared_chars(source, text)
    out_of = len(source)
    if len(text) > out_of:
        out_of = len(text)
    percentage = (shared / out_of) * 100
    return [shared, percentage]


def getLastLogs(amount):
    path = r'C:\Program Files (x86)\Pixel Mine\Ashen Empires\data\User_Data\*.log'
    files = glob.glob(path)
    lastestFile = max(files, key=os.path.getctime)
    lastLines = []
    with open(lastestFile, 'r') as file:
        lastLines = file.readlines()
    if amount > 0:
        return lastLines[-amount:]
    else:
        return lastLines


def getLastChannelLogs(channel, amount):
    logs = getLastLogs(0)
    systemLogs = []
    for log in logs:
        if f'({channel})' in log:
            systemLogs.append(log.replace('\n', '').strip())
    if amount > 0:
        return systemLogs[-amount:]
    else:
        return systemLogs


def checkLogsForMessage(chatLogs=[], text='fizzled.', textOpposite=''):
    # return [text for chatLog in chatLogs if text in chatLog]
    textFound = False
    for log in chatLogs:
        if f'({text})' in log:
            textFound = True
        elif textOpposite != '' and f'({textOpposite})' in log:
            textFound = False
    return textFound


def checkForChannelMessage(channel='System', text='fizzled.', amount=5):
    chatLogs = getLastChannelLogs(channel, amount)
    return [text for chatLog in chatLogs if text in chatLog]


def checkForComatMessage(text='fizzled.'):
    chatLogs = getLastChannelLogs('Combat/Magic', 3)
    return [text for chatLog in chatLogs if text in chatLog]


def getSelfFromParty(bot):
    result = None
    if len(bot.party_members_data) > 0:
        for partyMember in bot.party_members_data:
            if partyMember['name'] == 'Night Elf Male' or partyMember['name'] == 'Human Male':
                result = partyMember
                break
    return result


def getSelfIndex(bot):
    index = None
    if len(bot.party_members_data) > 0:
        for partyMember in bot.party_members_data:
            if partyMember['name'] == 'Night Elf Male' or partyMember['name'] == 'Human Male':
                index = partyMember['index']
                break
    return index


def getOnScreenLocation(bot, targetIndex):
    try:
        result = (None, None)
        selfIndex = getSelfIndex(bot)
        if selfIndex == None:
            return result
        selfCoords = bot.memory.GetPartyMemberLocation(selfIndex)
        if selfCoords[0] == None:
            return result
        targetCoords = bot.memory.GetPartyMemberLocation(targetIndex)
        if targetCoords[0] == None:
            return result

        # return none if character is on a different Z access
        if selfCoords[2] != targetCoords[2]:
            return result

        xOffset = abs(targetCoords[0] - selfCoords[0])
        yOffset = abs(targetCoords[1] - selfCoords[1])

        if xOffset < bot.consts.MIN_ONSCREEN_COORDS[0]:
            return result
        if yOffset < bot.consts.MIN_ONSCREEN_COORDS[1]:
            return result
        if xOffset > bot.consts.MAX_ONSCREEN_COORDS[0]:
            return result
        if yOffset > bot.consts.MAX_ONSCREEN_COORDS[1]:
            return result

        x = bot.consts.SELF_ONSCREEN_COORDS[0]
        y = bot.consts.SELF_ONSCREEN_COORDS[1]

        if targetCoords[0] > selfCoords[0]:
            x += (xOffset / 38)
        elif targetCoords[0] < selfCoords[0]:
            x -= (xOffset / 38)

        if targetCoords[1] > selfCoords[1]:
            # if our target is lower then us, target higher up on them
            y += (yOffset / 38) - 20
        elif targetCoords[1] < selfCoords[1]:
            # if our target is higher then us, target lower down on them
            y -= (yOffset / 38) + 20

        result = (x, y)
    except Exception as e:
        bot.log(f'[Logic] {traceback.format_exc()}')
    finally:
        return result


def getDistanceApart(bot, sourceCoords, targetCoords):
    try:
        result = (0, 0)
        # return none if character is on a different Z access
        if sourceCoords[2] != targetCoords[2]:
            return result

        xOffset = abs(targetCoords[0] - sourceCoords[0])
        yOffset = abs(targetCoords[1] - sourceCoords[1])

        if xOffset < bot.consts.MIN_ONSCREEN_COORDS[0]:
            return result
        if yOffset < bot.consts.MIN_ONSCREEN_COORDS[1]:
            return result
        if xOffset > bot.consts.MAX_ONSCREEN_COORDS[0]:
            return result
        if yOffset > bot.consts.MAX_ONSCREEN_COORDS[1]:
            return result

        if targetCoords[0] < sourceCoords[0]:
            xOffset = -abs(xOffset)
        if targetCoords[1] < sourceCoords[1]:
            yOffset = -abs(yOffset)

        result = (xOffset, yOffset)
    except Exception as e:
        bot.log(f'[Logic] {traceback.format_exc()}')
    finally:
        return result


def clickLocation(bot, x, y, offset=[48, 55]):
    if x != None and y != None:
        x += offset[0]
        y += offset[1]

        bot.controller.move_mouse(x, y)
        time.sleep(0.250)
        bot.controller.left_mouse_click(x, y)
        time.sleep(0.250)


def foundNpcIdAtPosition(bot, npcID, x, y):
    bot.controller.move_mouse(x, y, False)
    if bot.memory.GetMouseNPCId() == npcID:
        return True
    return False


def generateNpcRange(bot, baseX, baseY, TILE_SIZE):
    npcRange = [(baseX, baseY)]
    try:
        for x in range(5):
            for y in range(5):
                npcRange.append(
                    (baseX - (x * TILE_SIZE), baseY + (y * TILE_SIZE)))
            for y in range(5):
                npcRange.append(
                    (baseX + (x * TILE_SIZE), baseY + (y * TILE_SIZE)))
            for y in range(5):
                npcRange.append(
                    (baseX - (x * TILE_SIZE), baseY - (y * TILE_SIZE)))
            for y in range(5):
                npcRange.append(
                    (baseX + (x * TILE_SIZE), baseY - (y * TILE_SIZE)))
    except Exception as e:
        bot.log(f'[Logic] {traceback.format_exc()}')
    finally:
        return npcRange


def clickNpcID(bot, npcID, baseX, baseY, offset=[0, 0]):
    if baseX != None and baseY != None:
        foundID = False
        bot.log(
            f'clickNpcID [1]: npcID: {npcID}, baseX: {baseX}, baseY: {baseY}, offset: {offset}')

        mouseX, mouseY = bot.controller.getCursorPos()
        foundID = foundNpcIdAtPosition(
            bot, npcID, mouseX + offset[0], mouseY + offset[1])

        foundID = foundNpcIdAtPosition(
            bot, npcID, baseX + offset[0], baseY + offset[1])

        if not foundID:
            npcRange = sort_Tuple(generateNpcRange(
                bot, baseX, baseY, bot.consts.TILE_SIZE), 1)
            for nr in npcRange:
                if foundNpcIdAtPosition(bot, npcID, nr[0] + offset[0], nr[1] + offset[1]):
                    foundID = True
                    break

        bot.log(f'clickNpcID [6]: foundID: {foundID}')
        if foundID:
            bot.controller.left_mouse_click()
            time.sleep(0.250)


def canSeeObject(bot, template, threshold=0.9):
    try:
        matches = bot.vision.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1
    except:
        return False


def clickTemplate(bot, template, threshold=0.6, offset=[0, 0]):
    try:
        matches = bot.vision.find_template(template, threshold=threshold)

        if np.shape(matches)[1] >= 1:
            clickLocation(bot, matches[0][1], matches[0][1], offset=offset)
            time.sleep(0.250)
    finally:
        bot.vision.refresh_frame()


def clickSelf(bot):
    selfCoords = bot.consts.SELF_COORDS
    if selfCoords[0] != None:
        clickLocation(bot, selfCoords[0], selfCoords[1], offset=[0, 0])


def foundImage(bot, image, scales=[1.0, 0.9, 1.1]):
    bot.vision.refresh_frame(bot.consts.GAME_REGION)
    canSeeObject = False
    try:
        bot.vision.refresh_frame(bot.consts.GAME_REGION)
        matches = bot.vision.scaled_find_image(
            source=image, threshold=0.6, scales=scales)

        canSeeObject = np.shape(matches)[1] >= 1
    finally:
        bot.vision.refresh_frame()
        return canSeeObject


def findSelfOnScreen(bot):
    selfOnScreen = None

    bot.log('[Logic] Checking for own character on-screen...')
    if len(bot.party_members_data) > 0:
        for partyMember in bot.party_members_data:
            if partyMember['name'] == 'Night Elf Male' or partyMember['name'] == 'Human Male':
                partyMemberCoords = getOnScreenLocation(
                    bot, partyMember['index'])
                if partyMemberCoords[0] != None:
                    selfOnScreen = partyMember

    if selfOnScreen != None:
        bot.log(
            f'[Logic] Own character ({selfOnScreen["name"]}) detected on screen')

    return selfOnScreen


def findPartyMembersOnScreen(bot):
    partyMembersOnScreen = []

    bot.log('[Logic] Checking for party members on-screen...')
    if len(bot.party_members_data) > 0:
        for partyMember in bot.party_members_data:
            if partyMember['name'] == 'Night Elf Male' or partyMember['name'] == 'Human Male':
                continue

            partyMemberCoords = getOnScreenLocation(bot, partyMember['index'])
            if partyMemberCoords[0] != None:
                partyMembersOnScreen.append(partyMember)
    bot.log(
        f'[Logic] ({len(partyMembersOnScreen)}) Party members detected on-screen...')
    for x in partyMembersOnScreen:
        bot.log(f'[Logic] Party member ({x["name"]}) detected on screen')

    return partyMembersOnScreen


def replaceRunes(bot, ids):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)

    pyautogui.keyDown('shift')
    time.sleep(0.250)

    for id in ids:
        if id == bot.consts.Rune.BODY:
            bot.log(f'[Logic] Replacing Body Rune')
            pyautogui.press('f5')
        elif id == bot.consts.Rune.MALENOX:
            bot.log(f'[Logic] Replacing Malenox Rune')
            pyautogui.press('f6')
        elif id == bot.consts.Rune.AGON:
            bot.log(f'[Logic] Replacing Agon Rune')
            pyautogui.press('f7')
        elif id == bot.consts.Rune.MALITH:
            bot.log(f'[Logic] Replacing Malith Rune')
            pyautogui.press('f8')
        elif id == bot.consts.Rune.ULTHIEN:
            bot.log(f'[Logic] Replacing Ulthien Rune')
            pyautogui.press('f9')
        elif id == bot.consts.Rune.SABAL:
            bot.log(f'[Logic] Replacing Sabal Rune')
            pyautogui.press('f10')
        elif id == bot.consts.Rune.ISOS:
            bot.log(f'[Logic] Replacing Isos Rune')
            pyautogui.press('f11')
        elif id == bot.consts.Rune.VELDAN:
            bot.log(f'[Logic] Replacing Veldan Rune')
            pyautogui.press('f12')

    time.sleep(0.250)
    pyautogui.keyUp('shift')
    time.sleep(0.250)


def checkRunes(bot):
    Rune_slots = bot.memory.GetRuneSlots()
    indexes = []

    if Rune_slots > 0:
        Rune_types = bot.memory.GetRuneTypes()
        Rune_charges = bot.memory.GetRuneCharges()
        for index in range(Rune_slots - 1):
            charges = Rune_charges[index]
            time.sleep(0.100)
            if charges > 0 and charges <= 15:
                indexes.append(Rune_types[index])

    if len(indexes) > 0:
        replaceRunes(bot, indexes)


def getMissingHealthPercentage(memory):
    health_total = memory.GetMaxHealth()
    health_value = memory.GetCurHealth()
    if health_value == 0 or health_total == 0:
        return 0
    return int(100 * float(health_value)/float(health_total))


def useHealingPotion(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f4')


def useMagicalWeapon(bot):
    RuneSlots = bot.memory.GetRuneSlots()

    if bot.memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        bot.memory.SetHotbar(8)

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
    RuneTypes = bot.memory.GetRuneTypes()

    if bot.memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        bot.memory.SetHotbar(8)

    # If we aren't using a body Rune, switch to one
    if len(RuneTypes) > 0 and RuneTypes[0] != bot.consts.Rune.BODY:
        bot.log('[Logic] Switching Rune slot 0 to body')
        pyautogui.keyDown('shift')
        time.sleep(0.250)
        pyautogui.press('f5')
        time.sleep(0.250)
        pyautogui.keyUp('shift')
        time.sleep(0.250)


def useNonMagicalWeapon(bot):
    RuneSlots = bot.memory.GetRuneSlots()

    if bot.memory.GetHotbar() != 8:
        bot.log('[Logic] Switching to hotbar #8')
        bot.memory.SetHotbar(8)

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


def selectSpell(bot, spell_id=int, hotbar_key=str):
    while bot.memory.GetSpell() != spell_id:
        pyautogui.press(hotbar_key)
        time.sleep(0.250)


def prepareToHeal(bot):
    useMagicalWeapon(bot)
    useBodyRune(bot)


def prepareToAttack(bot):
    if bot.memory.GetSpell() != 0:
        pyautogui.press('f2')
    # useNonMagicalWeapon(bot)


def useHealingSpell(bot):
    prepareToHeal(bot)
    selectSpell(bot, bot.consts.Spell.SUPERIOR_HEAL, 'f2')

    bot.log('[Logic] Casting heal on self')
    clickSelf(bot)
    if checkForComatMessage('Your Superior Heal spell fizzled'):
        bot.log('[Logic] Superior Heal fizzled! Recasting...')
        clickSelf(bot)
    time.sleep(bot.consts.TIMER_SUPERIOR_HEAL)
    checkRunes(bot)


def useCallOfTheGodsSpell(bot):
    prepareToHeal(bot)
    selectSpell(bot, bot.consts.Spell.CALL_OF_THE_GODS, 'f6')

    bot.log('[Logic] Casting Call of the Gods on bot')
    clickSelf(bot)
    if checkForComatMessage('Your Call of the Gods spell fizzled'):
        bot.log('[Logic] Call of the Gods fizzled! Recasting...')
        clickSelf(bot)
    elif checkForComatMessage('You cannot cast Call of the Gods for another'):
        bot.log(
            '[Logic] Call of the Gods on cooldown! Switching to Superior Heal')
        return useHealingSpell(bot)
    time.sleep(bot.consts.TIMER_SUPERIOR_HEAL)
    checkRunes(bot)


def useStaminaPotion(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f3')


def healPartyMember(bot, partyMember):
    try:
        if not 'name' in partyMember:
            return

        bot.active_party_member_name = partyMember['name']
        prepareToHeal(bot)

        while bot.memory.GetSpell() != bot.consts.Spell.SUPERIOR_HEAL:
            pyautogui.press('f2')
            time.sleep(0.250)

        selfCoords = bot.consts.SELF_ONSCREEN_COORDS
        selfIndex = getSelfIndex(bot)
        if selfIndex == None:
            return
        selfLocation = bot.memory.GetPartyMemberLocation(selfIndex)
        if selfLocation[0] == None:
            return
        memberLocation = bot.memory.GetPartyMemberLocation(
            partyMember['index'])
        if memberLocation[0] == None:
            return

        xDif, yDif = getDistanceApart(bot, selfLocation, memberLocation)

        xOffset = 0
        yOffset = 0
        if xDif < 0:
            xOffset = -abs(xDif * bot.consts.TILE_SIZE)
        else:
            xOffset = abs(xDif * bot.consts.TILE_SIZE)

        if yDif < 0:
            yOffset = -abs(yDif * bot.consts.TILE_SIZE)
        else:
            yOffset = abs(yDif * bot.consts.TILE_SIZE)

        bot.log(f'[Logic] selfCoords: {selfCoords}')
        bot.log(f'[Logic] selfLocation: {selfLocation}')
        bot.log(f'[Logic] memberLocation: {memberLocation}')
        bot.log(f'[Logic] xDif: {xDif}, yDif: {yDif}')
        bot.log(f'[Logic] xOffset: {xOffset}, yOffset: {yOffset}')

        bot.log(
            f'[Logic] Casting superior heal on party member [{partyMember["name"]}] (priority: {partyMember["priority"]})')
        clickNpcID(bot, partyMember['npcID'], selfCoords[0],
                   selfCoords[1], offset=[xOffset, yOffset])

        if checkForComatMessage('Your Superior Heal spell fizzled'):
            bot.log('[Logic] Spell fizzled! Recasting...')
            clickNpcID(bot, partyMember['npcID'], selfCoords[0],
                       selfCoords[1], offset=[xOffset, yOffset])

        time.sleep(bot.consts.TIMER_SUPERIOR_HEAL)
        checkRunes(bot)
    except Exception as e:
        bot.log(f'[Logic] {traceback.format_exc()}')


def useFood(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f9')


def useRegenerationTotem(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f10')


def useClassTotem(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f11')


def useWerewolfTotem(bot):
    if bot.memory.GetHotbar() != 8:
        bot.memory.SetHotbar(8)
    pyautogui.press('f12')


def getNewTarget(bot):
    if bot.memory.GetTargetId() > 0:
        return

    prepareToAttack(bot)

    bot.log('[Attacker] Looking for a new target...')
    bot.looking_for_target = True
    for i in range(30):
        if bot.state != 1:
            target = -1
            break
        pyautogui.press("`")
        time.sleep(0.250)
        if bot.memory.GetTargetId() > 0:
            bot.log(f'[Logic] Mew target found!')
            break
        else:
            time.sleep(0.500)

    bot.looking_for_target = False


def getPartyMemberToHeal(bot):
    if bot.last_party_count == 0:
        return

    memberToHeal = {'priority': -1}
    bot.log('[Logic] Checking if any party member needs healing...')

    doesAMemberNeedHealing = False
    for partyMember in bot.party_members_data:
        if partyMember['name'] == 'Night Elf Male':
            continue

        if 'priority' in partyMember:
            if partyMember['priority'] > 0:
                doesAMemberNeedHealing = True

    # Check if anyone needs healing in the party
    # if not doesAMemberNeedHealing:
    #    return

    bot.party_members_on_screen = findPartyMembersOnScreen(bot)
    if len(bot.party_members_on_screen) == 0:
        return

    bot.log(
        '[Logic] Checking for the party member on-screen with the highest priority level...')
    for partyMember in bot.party_members_on_screen:
        try:
            if bot.state != 1:
                break

            priority = partyMember['priority']

            # If our last target still needs heals, continue healing them first
            if bot.active_party_member_name != '':
                if partyMember['name'] == bot.active_party_member_name and priority > 0:
                    memberToHeal = partyMember
                    break

            if priority >= 5:  # Priority is 5 or more, so ignore all other checks
                memberToHeal = partyMember
                break
            elif priority > memberToHeal['priority']:
                memberToHeal = partyMember
        except Exception as e:
            bot.log(f'[Logic] {traceback.format_exc()}')
            continue

    if 'name' in memberToHeal:
        partyMemberName = memberToHeal["name"]
        bot.log(
            f'[Logic] Party member to heal: {partyMemberName} (priority: {memberToHeal["priority"]})')
        healPartyMember(bot, memberToHeal)
    else:
        bot.active_party_member_name = ''
        bot.log(
            f'[Logic] Failed to find any party members needing healing on the screen')


def getPartyMembersPriority(bot, partyMember):
    healthColor = (239, 74, 74)
    priority = 0
    try:
        if bot.state != 1:
            return partyMember
        locX = int(partyMember['gui']['left'] + 132)
        locY = int(partyMember['gui']['top'] + 3)

        if ImageGrab.grab().getpixel((locX, locY)) != healthColor:
            priority = 1
            if not ImageGrab.grab().getpixel((locX - 5, locY)) == healthColor:
                priority = 2
                if not ImageGrab.grab().getpixel((locX - 10, locY)) == healthColor:
                    priority = 3
                    if not ImageGrab.grab().getpixel((locX - 15, locY)) == healthColor:
                        priority = 4
                        if not ImageGrab.grab().getpixel((locX - 20, locY)) == healthColor:
                            priority = 5
                            if not ImageGrab.grab().getpixel((locX - 25, locY)) == healthColor:
                                priority = 6
    except Exception as e:
        bot.log(f'[Logic] {traceback.format_exc()}')
    finally:
        return priority


def updatePartyMembersData(bot):
    partyCount = bot.last_party_count
    bot.log(f'[Logic] Updating party members coords: [{partyCount}]')

    for party_member in bot.party_members_data:
        party_member['priority'] = getPartyMembersPriority(
            bot, party_member)


def getPartyMembersData(bot):
    partyCount = bot.last_party_count
    partyNames = []
    party_data = []
    bot.log(f'[Logic] Updating party members data: [{partyCount}]')
    if partyCount > 0:
        matches = bot.vision.find_template('gui-party-top', threshold=0.6)

        if np.shape(matches)[1] >= 1:
            offset = [35, 22]
            x = matches[1][0] + offset[1]
            y = matches[0][0] + offset[0]

            party_data = bot.memory.GetPartyMemberData()
            for party_member in party_data:
                offSetY = int(party_member['index'] * 15)
                party_member['gui'] = {'top': y + offSetY, 'left': x}
                party_member['priority'] = 0
                partyNames.append(party_member['name'])

    bot.party_members_data = party_data
    bot.log(f'[Logic] PartyMembers: {partyNames}')
    if len(party_data) > 0:
        bot.log(f'[Logic] PartyMembers Data: {party_data}')
