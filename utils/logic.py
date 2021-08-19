import os
import time
import glob
import traceback
import pyautogui
import numpy as np
from PIL import ImageGrab

from tkinter import *


def getLastLogs(amount):
    path = r'C:\Program Files (x86)\Pixel Mine\Ashen Empires\data\User_Data\*.log'
    files = glob.glob(path)
    lastestFile = max(files, key=os.path.getctime)
    lastLines = []
    with open(lastestFile, 'r') as file:
        lines = file.readlines()
        if amount > 0:
            lastLines = lines[amount:]
        else:
            lastLines = lines
    return lastLines


def getLastChannelLogs(channel, amount):
    logs = getLastLogs(amount)
    systemLogs = []
    for log in logs:
        if f'({channel})' in log:
            systemLogs.append(log)
    if amount > 0:
        return systemLogs[amount:]
    else:
        return systemLogs


def canSeeObject(bot, template, threshold=0.9):
    matches = bot.vision.find_template(template, threshold=threshold)
    return np.shape(matches)[1] >= 1


def clickObject(bot, template, offset=(0, 0)):
    matches = bot.vision.find_template(template)

    x = matches[1][0] + offset[0]
    y = matches[0][0] + offset[1]

    bot.controller.move_mouse(x, y)
    bot.controller.left_mouse_click()

    time.sleep(0.5)


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


def checkForFizzle():
    chatLogs = getLastChannelLogs('Combat/Magic', 3)
    return 'fizzled.' in chatLogs


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


def clickPartyMember(bot, image, scales=[1.0, 0.9, 1.1]):
    bot.vision.refresh_frame(bot.consts.game_region)
    matches = bot.vision.scaled_find_image(
        source=image, threshold=0.6, scales=scales)

    if np.shape(matches)[1] >= 1:
        offsets = [45, 125]
        x = matches[1][0] + offsets[0]
        y = matches[0][0] + offsets[1]

        bot.controller.move_mouse(x, y)
        time.sleep(0.250)
        bot.controller.left_mouse_click()
        time.sleep(0.5)

    bot.vision.refresh_frame()


def clickSelf(bot):
    bot.vision.refresh_frame(bot.consts.game_region)
    matches = bot.vision.scaled_find_template(
        'own-name', threshold=0.6)

    if np.shape(matches)[1] >= 1:
        offsets = [45, 125]
        x = matches[1][0] + offsets[0]
        y = matches[0][0] + offsets[1]

        bot.controller.move_mouse(x, y)
        time.sleep(0.250)
        bot.controller.left_mouse_click()
        time.sleep(0.5)

    bot.vision.refresh_frame()


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
    if not 'image' in partyMember:
        return

    partyMemberName = partyMember['name']
    partyMemberImage = partyMember['image']
    partyMemberImageCropped = partyMember['cropped']
    if foundImage(bot, partyMemberImage, scales=[0.5, 0.8, 1.0]):
        bot.log(
            f'[Logic] Casting call of the gods on party member [{partyMemberName}]')
        bot.memory.SetHotbar(8)
        if bot.memory.GetSpell() != bot.consts.spell_superior:
            pyautogui.press('f2')
        clickPartyMember(bot, partyMemberImage, scales=[0.5, 0.8, 1.0])
        if checkForFizzle():
            bot.log('[Logic] Spell fizzled! Recasting...')
            return healPartyMember(bot, partyMember)
        else:
            time.sleep(bot.consts.timer_spell_superior)
            checkRunes(bot)
    elif foundImage(bot, partyMemberImageCropped, scales=[0.5, 0.8, 1.0, 1.2, 1.5, 2.0]):
        bot.log(
            f'[Logic] Casting call of the gods on party member [{partyMemberName}]')
        bot.memory.SetHotbar(8)
        if bot.memory.GetSpell() != bot.consts.spell_superior:
            pyautogui.press('f2')
        clickPartyMember(bot, partyMemberImageCropped, scales=[
                         0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
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

    priorityPartyMember = {'name': '', 'hp': 0}
    healthColor = (239, 74, 74)

    for partyMember in bot.party_member_data:
        try:
            if bot.state != 'running':
                break
            locX = int(partyMember['pos']['left'] + 128)
            locY = int(partyMember['pos']['top'] + 3)
            health = 0

            if ImageGrab.grab().getpixel((locX, locY)) != healthColor:
                health = 1
                if not ImageGrab.grab().getpixel((locX - 5, locY)) == healthColor:
                    health = 2
                    if not ImageGrab.grab().getpixel((locX - 10, locY)) == healthColor:
                        health = 3
                        if not ImageGrab.grab().getpixel((locX - 15, locY)) == healthColor:
                            health = 4
                            if not ImageGrab.grab().getpixel((locX - 20, locY)) == healthColor:
                                health = 5
                if health > priorityPartyMember['hp']:
                    if foundImage(bot, partyMember['image']) or foundImage(bot, partyMember['cropped']):
                        priorityPartyMember = {
                            'image': partyMember['image'], 'cropped': partyMember['cropped'], 'name': partyMember['name'], 'hp': health}
        except Exception as e:
            bot.log(f'[Logic] {traceback.format_exc()}')
            continue

    if 'image' in priorityPartyMember:
        partyMemberName = priorityPartyMember["name"]
        bot.log(f'[Logic] PartyMemberToHeal: {partyMemberName}')
        healPartyMember(bot, priorityPartyMember)


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
                    monitor={'top': y + offSetY, 'left': x, 'width': 80, 'height': 13}, blackAndWhite=True, crop=False, scale=5.0)
                partyMemberImageCrop = bot.vision.take_screenshot(
                    monitor={'top': y + offSetY, 'left': x, 'width': 80, 'height': 13}, blackAndWhite=True, crop=True, scale=1.7)
                if len(partyMemberImage) > 0:
                    partyMemberData = {'image': partyMemberImage, 'cropped': partyMemberImageCrop, 'name': bot.ocr.textFromImage(partyMemberImage).replace('\n\x0c', '').strip(), 'pos': {
                        'top': y + offSetY, 'left': x}}
                    memberNames.append(partyMemberData['name'])
                    bot.party_member_data.append(partyMemberData)
        bot.log(f'[Logic] PartyMembers: {memberNames}')
