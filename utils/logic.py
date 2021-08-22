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


def checkForComatMessage(text='fizzled.'):
    chatLogs = getLastChannelLogs('Combat/Magic', 3)
    return text in chatLogs


def clickLocation(bot, x, y, offset=[48, 55]):
    if x != None and y != None:
        x += offset[0]
        y += offset[1]

        bot.controller.move_mouse(x, y)
        time.sleep(0.250)
        bot.controller.left_mouse_click()
        time.sleep(0.5)


def canSeeObject(bot, template, threshold=0.9):
    try:
        matches = bot.vision.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1
    except:
        return False


def clickObject(bot, template, threshold=0.6, offset=[0, 0]):
    try:
        matches = bot.vision.find_template(template, threshold=0.6)

        if np.shape(matches)[1] >= 1:
            clickLocation(bot, matches[0][1], matches[0][1], offset=[0, 0])
            time.sleep(0.5)
    finally:
        bot.vision.refresh_frame()


def clickSelf(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    try:
        matches = []
        canSeeObject = False

        for template in ['own-name', 'own-name-alt']:
            template_matches = bot.vision.find_template_matches(
                template, monitor=bot.consts.game_region, threshold=0.6)
            canSeeObject = len(template_matches) > 0 and np.shape(
                template_matches)[1] >= 1
            if canSeeObject:
                matches = template_matches
                break

        if canSeeObject:
            clickLocation(bot, matches[0][0], matches[0][1], offset=[45, 125])
    finally:
        bot.vision.refresh_frame()


def clickAlt(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    try:
        matches = []
        canSeeObject = False

        for template in bot.alt_character['templates']:
            template_matches = bot.vision.find_template_matches(
                template, monitor=bot.consts.game_region, threshold=0.6)
            canSeeObject = len(template_matches) > 0 and np.shape(
                template_matches)[1] >= 1
            if canSeeObject:
                matches = template_matches
                break

        if canSeeObject:
            clickLocation(bot, matches[0][0], matches[0][1], offset=[45, 125])
    finally:
        bot.vision.refresh_frame()


def foundSelf(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    canSeeObject = False
    try:
        for template in ['own-name', 'own-name-alt']:
            template_matches = bot.vision.find_template_matches(
                template, monitor=bot.consts.game_region, threshold=0.6)
            canSeeObject = len(template_matches) > 0 and np.shape(
                template_matches)[1] >= 1
            if canSeeObject:
                break
    finally:
        bot.vision.refresh_frame()
        return canSeeObject


def foundAlt(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    canSeeObject = False
    try:
        for template in bot.alt_character['templates']:
            template_matches = bot.vision.find_template_matches(
                template, monitor=bot.consts.game_region, threshold=0.6)
            canSeeObject = len(template_matches) > 0 and np.shape(
                template_matches)[1] >= 1
            if canSeeObject:
                break
    finally:
        bot.vision.refresh_frame()
        return canSeeObject


def foundPartyWindow(bot):
    bot.vision.refresh_frame()
    canSeeObject = False
    try:
        matches = bot.vision.scaled_find_template(
            'gui-party-top', threshold=0.6)
        canSeeObject = np.shape(matches)[1] >= 1
    finally:
        return canSeeObject


def foundImage(bot, image, scales=[1.0, 0.9, 1.1]):
    bot.vision.refresh_frame(bot.consts.game_region)
    canSeeObject = False
    try:
        bot.vision.refresh_frame(bot.consts.game_region)
        matches = bot.vision.scaled_find_image(
            source=image, threshold=0.6, scales=scales)

        canSeeObject = np.shape(matches)[1] >= 1
    finally:
        bot.vision.refresh_frame()
        return canSeeObject


def updateAltCharacterData(bot):
    bot.alt_character['priority'] = 0
    for partyMember in bot.party_member_data:
        partyName = partyMember['name']
        shared, percentage = compare_strings(
            partyName, bot.consts.alt_character['name'])

        if percentage > 70:
            bot.alt_character['priority'] = partyMember['priority']


def findPartyMembersOnScreen(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    partyMembersOnScreen = []
    matches = []

    guild_tag_templates = ['guild-tag-left0', 'guild-tag-left1', 'guild-tag-left2',
                           'guild-tag-left3', 'guild-tag-left4', 'guild-tag-left5', 'guild-tag-left6']
    for template in guild_tag_templates:
        template_matches = bot.vision.find_template_matches(
            template, monitor=bot.consts.game_region, threshold=0.6)
        canSeeObject = len(template_matches) > 0 and np.shape(
            template_matches)[1] >= 1
        if canSeeObject:
            matches = template_matches
            break

    bot.log('[Logic] Checking for any guild tags and party members on-screen...')
    if len(matches) > 0:
        for match in matches:
            top = match[1] + 71
            left = match[0] + 28
            memberImage = bot.vision.take_screenshot(
                monitor={'top': top, 'left': left, 'width': 120, 'height': 20}, blackAndWhite=False, crop=False, scale=5.0)
            bot.vision.show_image(memberImage, 'tag')
            memberName = bot.ocr.textFromImage(memberImage)
            if memberName == '':
                continue

            for partyMember in bot.party_member_data:
                partyName = partyMember['name']
                shared, percentage = compare_strings(partyName, memberName)

                if percentage > 70:
                    partyMember['game_window'] = {'x': left,
                                                  'y': top, 'image': memberImage}
                    partyMembersOnScreen.append(partyMember)
    bot.log(f'[Logic] ({len(matches)}) Guild tags detected on-screen...')
    bot.log(
        f'[Logic] ({len(partyMembersOnScreen)}) Party members detected on-screen...')
    for x in partyMembersOnScreen:
        bot.log(f'[Logic] Party member ({x["name"]}) detected on screen')

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
    if foundSelf(bot):
        bot.memory.SetHotbar(8)
        while bot.memory.GetSpell() != bot.consts.spell_superior:
            pyautogui.press('f2')
            time.sleep(0.250)
        bot.log('[Logic] Casting heal on bot')
        clickSelf(bot)
        if checkForComatMessage('Your Superior Heal spell fizzled'):
            bot.log('[Logic] Superior Heal fizzled! Recasting...')
            return useHealingSpell(bot)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)


def useCallOfTheGodsSpell(bot):
    if foundSelf(bot):
        bot.memory.SetHotbar(8)
        while bot.memory.GetSpell() != bot.consts.spell_cog:
            pyautogui.press('f6')
            time.sleep(0.250)
        bot.log('[Logic] Casting Call of the Gods on bot')
        clickSelf(bot)
        if checkForComatMessage('Your Call of the Gods spell fizzled'):
            bot.log('[Logic] Call of the Gods fizzled! Recasting...')
            return useCallOfTheGodsSpell(bot)
        elif checkForComatMessage('You cannot cast Call of the Gods for another'):
            bot.log(
                '[Logic] Call of the Gods on cooldown! Switching to Superior Heal')
            return useHealingSpell(bot)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)


def useHealingSpellOnAlt(bot):
    bot.memory.SetHotbar(8)
    while bot.memory.GetSpell() != bot.consts.spell_superior:
        pyautogui.press('f2')
        time.sleep(0.250)
    if foundAlt(bot):
        bot.log(f'[Logic] Casting heal on {bot.alt_character["name"]}')
        clickAlt(bot)
        if checkForComatMessage('Your Superior Heal spell fizzled'):
            bot.log('[Logic] Superior Heal fizzled! Recasting...')
            return useHealingSpellOnAlt(bot)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)


def useStaminaPotion(bot):
    bot.memory.SetHotbar(8)
    pyautogui.press('f4')


def healPartyMember(bot, partyMember):
    if not 'name' in partyMember:
        return

    bot.memory.SetHotbar(8)
    while bot.memory.GetSpell() != bot.consts.spell_superior:
        pyautogui.press('f2')
        time.sleep(0.250)
    bot.log(
        f'[Logic] Casting superior heal on party member [{partyMember["name"]}] (priority: {partyMember["priority"]})')
    clickLocation(bot, partyMember['x'], partyMember['y'], offset=[48, 55])
    if checkForComatMessage('Your Superior Heal spell fizzled'):
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
    bot.log('[Logic] Checking if any party member needs healing...')

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

    bot.log(
        '[Logic] Checking for the party member on-screen with the highest priority level...')
    for partyMember in bot.party_members_on_screen:
        try:
            if bot.state != 'running':
                break

            locX = partyMember['game_window']['x']
            locY = partyMember['game_window']['y']
            priority = partyMember['priority']

            if priority == 5:  # Priority is 5, so ignore all other checks
                memberToHeal = {
                    'name': partyMember['name'], 'x': locX, 'y': locY, 'priority': priority}
                break
            elif priority > memberToHeal['priority']:
                memberToHeal = {
                    'name': partyMember['name'], 'x': locX, 'y': locY, 'priority': priority}
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
    bot.log('[Logic] Checking the health levels of all members in the party list...')
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
    partyCount = bot.last_party_count
    partyNames = []
    party_data = []
    bot.log(f'[Logic] Updating party member images: [{partyCount}]')
    if partyCount > 0:
        matches = bot.vision.find_template('gui-party-top', threshold=0.6)

        if np.shape(matches)[1] >= 1:
            offset = [35, 22]
            x = matches[1][0] + offset[1]
            y = matches[0][0] + offset[0]

            party_data = []
            for i in range(partyCount):
                offSetY = int(i * 15)
                partyMemberImage = bot.vision.take_screenshot(
                    monitor={'top': y + offSetY, 'left': x, 'width': 80, 'height': 13}, blackAndWhite=False, crop=False, scale=5.0)
                if len(partyMemberImage) > 0:
                    name = bot.ocr.textFromImage(partyMemberImage)
                    if name != '':
                        partyMemberData = {'name': name, 'party': {
                            'top': y + offSetY, 'left': x}, 'priority': 0}
                        partyNames.append(partyMemberData['name'])
                        party_data.append(partyMemberData)

    bot.party_member_data = party_data
    bot.log(f'[Logic] PartyMembers: {partyNames}')
