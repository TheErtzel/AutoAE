import os
import time
import glob
import traceback
import pyautogui
import numpy as np
from PIL import ImageGrab
from collections import Counter

from tkinter import *


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


def checkForFizzle():
    chatLogs = getLastChannelLogs('Combat/Magic', 3)
    return 'fizzled.' in chatLogs


def clickLocation(bot, x, y, offset=[48, 55]):
    if x != None and y != None:
        x += offset[0]
        y += offset[1]

        bot.controller.move_mouse(x, y)
        time.sleep(0.250)
        bot.controller.left_mouse_click()
        time.sleep(0.5)


def canSeeObject(bot, template, threshold=0.9):
    matches = bot.vision.find_template(template, threshold=threshold)
    return np.shape(matches)[1] >= 1


def clickObject(bot, template, threshold=0.6, offset=[0, 0]):
    matches = bot.vision.find_template(template, threshold=0.6)

    if np.shape(matches)[1] >= 1:
        clickLocation(bot, matches[1][0], matches[0][0], offset=[0, 0])

    bot.controller.move_mouse(x, y)
    bot.controller.left_mouse_click()

    time.sleep(0.5)


def clickSelf(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    matches = bot.vision.scaled_find_template(
        'own-name', threshold=0.6)

    if np.shape(matches)[1] >= 1:
        clickLocation(bot, matches[1][0], matches[0][0], offset=[45, 125])

    bot.vision.refresh_frame()


def foundSelf(bot):
    bot.vision.refresh_frame(bot.consts.game_region)

    matches = bot.vision.scaled_find_template(
        'own-name', threshold=0.6)
    canSeeObject = np.shape(matches)[1] >= 1

    bot.vision.refresh_frame()
    return canSeeObject


def foundPartyWindow(bot):
    matches = bot.vision.scaled_find_template(
        'gui-party-top', threshold=0.6)
    canSeeObject = np.shape(matches)[1] >= 1

    return canSeeObject


def foundImage(bot, image, scales=[1.0, 0.9, 1.1]):
    bot.vision.refresh_frame(bot.consts.game_region)
    matches = bot.vision.scaled_find_image(
        source=image, threshold=0.6, scales=scales)

    canSeeObject = np.shape(matches)[1] >= 1

    bot.vision.refresh_frame()
    return canSeeObject


def findPartyMembersOnScreen(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    partyMembersOnScreen = []
    matches = bot.vision.find_template_matches(
        'party-name-left-light', monitor=bot.consts.game_region, threshold=0.6)

    if len(matches) == 0:
        matches = bot.vision.find_template_matches(
            'party-name-left-dark', monitor=bot.consts.game_region, threshold=0.6)

    for match in matches:
        top = match[1] + 71
        left = match[0] + 28
        memberImage = bot.vision.take_screenshot(
            monitor={'top': top, 'left': left, 'width': 120, 'height': 20}, blackAndWhite=False, crop=False, scale=5.0)
        memberName = bot.ocr.textFromImage(memberImage)
        for partyMember in bot.party_member_data:
            partyName = partyMember['name']
            shared, percentage = compare_strings(partyName, memberName)

            if percentage > 70:
                bot.log(
                    f'[Logic] (findPartyMembersOnScreen) Party Name: {partyName} [{len(partyName)}]')
                bot.log(
                    f'[Logic] (findPartyMembersOnScreen) On-screen Name: {memberName} [{len(memberName)}]')
                bot.log(
                    f'[Logic] (findPartyMembersOnScreen) Shared characters: {shared}')
                bot.log(
                    f'[Logic] (findPartyMembersOnScreen) Similarity {percentage} %')

                partyMember['game_window'] = {'x': left,
                                              'y': top, 'image': memberImage}
                partyMembersOnScreen.append(partyMember)

    bot.vision.refresh_frame()
    return partyMembersOnScreen


def replaceRunes(bot, ids):
    bot.memory.SetHotbar(8)
    pyautogui.keyDown('shift')
    time.sleep(0.250)

    for id in ids:
        if id == bot.consts.rune_id_Body:
            bot.log(f'[Logic] Replacing Body rune')
            pyautogui.press('f5')
        elif id == bot.consts.rune_id_Malenox:
            bot.log(f'[Logic] Replacing Malenox rune')
            pyautogui.press('f6')
        elif id == bot.consts.rune_id_Agon:
            bot.log(f'[Logic] Replacing Agon rune')
            pyautogui.press('f7')
        elif id == bot.consts.rune_id_Malith:
            bot.log(f'[Logic] Replacing Malith rune')
            pyautogui.press('f8')
        elif id == bot.consts.rune_id_Ulthien:
            bot.log(f'[Logic] Replacing Ulthien rune')
            pyautogui.press('f9')
        elif id == bot.consts.rune_id_Sabal:
            bot.log(f'[Logic] Replacing Sabal rune')
            pyautogui.press('f10')
        elif id == bot.consts.rune_id_Isos:
            bot.log(f'[Logic] Replacing Isos rune')
            pyautogui.press('f11')
        elif id == bot.consts.rune_id_Veldan:
            bot.log(f'[Logic] Replacing Veldan rune')
            pyautogui.press('f12')

    time.sleep(0.250)
    pyautogui.keyUp('shift')
    time.sleep(0.250)


def checkRunes(bot):
    rune_slots = bot.memory.GetRuneSlots()
    indexes = []

    if rune_slots > 0:
        rune_types = bot.memory.GetRuneTypes()
        rune_charges = bot.memory.GetRuneCharges()
        for index in range(rune_slots - 1):
            charges = rune_charges[index]
            time.sleep(0.100)
            if charges > 0 and charges <= 15:
                indexes.append(rune_types[index])

    if len(indexes) > 0:
        replaceRunes(bot, indexes)


def getMissingHealthPercentage(memory):
    health_total = memory.GetMaxHealth()
    health_value = memory.GetCurHealth()
    if health_value == 0 or health_total == 0:
        return 0
    return int(100 * float(health_value)/float(health_total))


def useHealingPotion(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f4')


def useHealingSpell(bot):
    bot.memory.SetHotbar(8)
    if bot.memory.GetSpell() != bot.consts.spell_superior:
        pyautogui.press('f2')
    if foundSelf():
        bot.log('[Logic] Casting heal on bot')
        clickSelf(bot)
        if checkForFizzle():
            bot.log('[Logic] Spell fizzled! Recasting...')
            return useHealingSpell(bot)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)


def useCallOfTheGodsSpell(bot):
    bot.memory.SetHotbar(8)
    if bot.memory.GetSpell() != bot.consts.spell_cog:
        pyautogui.press('f6')
    if foundSelf():
        bot.log('[Logic] Casting call of the gods on bot')
        clickSelf(bot)
        if checkForFizzle():
            bot.log('[Logic] Spell fizzled! Recasting...')
            return useCallOfTheGodsSpell(bot)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)


def useStaminaPotion(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f4')


def healPartyMember(bot, partyMember):
    if not 'name' in partyMember:
        return

    bot.log(
        f'[Logic] Casting superior heal on party member [{partyMember["name"]}]')
    bot.memory.SetHotbar(8)
    if bot.memory.GetSpell() != bot.consts.spell_superior:
        pyautogui.press('f2')
    clickLocation(bot, partyMember['x'], partyMember['y'], offsets=[48, 55])
    if checkForFizzle():
        bot.log('[Logic] Spell fizzled! Recasting...')
        return healPartyMember(bot, partyMember)
    else:
        time.sleep(bot.consts.timer_spell_superior)
        checkRunes(bot)


def useFood(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f9')


def useRegenerationTotem(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f10')


def useClassTotem(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f11')


def useWerewolfTotem(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f12')


def getPartyMemberToHeal(bot):
    if bot.last_party_count == 0:
        return

    memberToHeal = {'priority': 0, 'x': 0, 'y': 0}

    doesAMemberNeedHealing = False
    for partyMember in bot.party_member_data:
        if 'priority' in partyMember:
            if partyMember['priority'] > 0:
                doesAMemberNeedHealing = True

    # Check if anyone needs healing in the party
    if not doesAMemberNeedHealing:
        return

    bot.party_members_on_screen = findPartyMembersOnScreen(bot)
    if len(bot.party_members_on_screen) == 0:
        return

    for partyMember in bot.party_members_on_screen:
        try:
            if bot.state != 'running':
                break

            locX = partyMember['game_window']['x']
            locY = partyMember['game_window']['y']

            if partyMember['priority'] == 5:  # Priority is 5, so ignore all other checks
                memberToHeal = {
                    'name': partyMember['name'], 'x': locX, 'y': locY}
                break
            elif partyMember['priority'] > memberToHeal['priority']:
                memberToHeal = {
                    'name': partyMember['name'], 'x': locX, 'y': locY}
        except Exception as e:
            bot.log(f'[Logic] {traceback.format_exc()}')
            continue

    if 'name' in memberToHeal:
        partyMemberName = memberToHeal["name"]
        bot.log(f'[Logic] Party member to heal: {partyMemberName}')
        healPartyMember(bot, memberToHeal)
    else:
        bot.log(
            f'[Logic] Failed to find any party members needing healing on the screen')


def updatePartyMemberHealths(bot):
    if bot.last_party_count == 0:
        return

    healthColor = (239, 74, 74)
    for partyMember in bot.party_member_data:
        try:
            if bot.state != 'running':
                break
            locX = int(partyMember['party']['left'] + 128)
            locY = int(partyMember['party']['top'] + 3)
            priority = 0

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
                partyMember['priority'] = priority
        except Exception as e:
            bot.log(f'[Logic] {traceback.format_exc()}')
            continue


def updatePartyMemberData(bot):
    memberCount = bot.last_party_count
    memberNames = []
    bot.log(f'[Logic] Updating party member images: [{memberCount}]')
    if memberCount > 0:
        matches = bot.vision.find_template('gui-party-top', threshold=0.6)

        if np.shape(matches)[1] >= 1:
            offsets = [35, 22]
            x = matches[1][0] + offsets[1]
            y = matches[0][0] + offsets[0]

            bot.party_member_data = []
            for i in range(memberCount):
                offSetY = int(i * 15)
                partyMemberImage = bot.vision.take_screenshot(
                    monitor={'top': y + offSetY, 'left': x, 'width': 80, 'height': 13}, blackAndWhite=False, crop=False, scale=5.0)
                if len(partyMemberImage) > 0:
                    partyMemberData = {'name': bot.ocr.textFromImage(partyMemberImage), 'party': {
                        'top': y + offSetY, 'left': x}, 'priority': 0}
                    memberNames.append(partyMemberData['name'])
                    bot.party_member_data.append(partyMemberData)
        bot.log(f'[Logic] PartyMembers: {memberNames}')
