import numpy as np
import time
import keyboard
import pyautogui

import utils.shared as shared

class Game:
    def __init__(self, consts, memory, vision, controller):
        self.consts = consts
        self.memory = memory
        self.vision = vision
        self.controller = controller
        self.state = 'paused'

        self.log('Started! press pause to toggle pause/un-pause')

        keyboard.add_hotkey('pause', self.toggle_pause)

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))

    def toggle_pause(self):
        if self.state == 'paused': 
            self.state = 'started'
            self.log('Un-paused')
        else: 
            self.state = 'paused'
            self.log('Paused')
        time.sleep(0.500)

    def can_see_object(self, template, threshold=0.9):
        matches = self.vision.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def click_object(self, template, offset=(0, 0)):
        matches = self.vision.find_template(template)

        x = matches[1][0] + offset[0]
        y = matches[0][0] + offset[1]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)
        
    def found_health_bar(self):
        return self.can_see_object('health-bar')
        
    def found_stamina_bar(self):
        return self.can_see_object('stamina-bar')
        
    def found_party_member(self):
        self.vision.refresh_frame({'top': 70, 'left': 10, 'width': 790, 'height': 530})
        
        matches = self.vision.scaled_find_template('party-member-name', threshold=0.7)
        canSeeObject = np.shape(matches)[1] >= 1

        self.vision.refresh_frame()
        return canSeeObject
        
    def click_party_member(self):
        self.vision.refresh_frame({'top': 70, 'left': 10, 'width': 790, 'height': 530})        
        matches = self.vision.find_template('party-member-name', threshold=0.6)

        if np.shape(matches)[1] >= 1:
            #offsets = self.consts._partyMemberOffset
            offsets = [45, 125]
            x = matches[1][0] + offsets[0]
            y = matches[0][0] + offsets[1]

            self.controller.move_mouse(x, y)
            time.sleep(0.250)
            self.controller.left_mouse_click()
            time.sleep(0.5)

        self.vision.refresh_frame()
        
    def found_self(self):
        self.vision.refresh_frame({'top': 70, 'left': 10, 'width': 790, 'height': 530})
        
        matches = self.vision.scaled_find_template('own-name', threshold=0.7)
        canSeeObject = np.shape(matches)[1] >= 1

        self.vision.refresh_frame()
        return canSeeObject
        
    def click_self(self):
        self.vision.refresh_frame({'top': 70, 'left': 10, 'width': 790, 'height': 530})        
        matches = self.vision.find_template('own-name', threshold=0.6)

        if np.shape(matches)[1] >= 1:
            #offsets = self.consts._partyMemberOffset
            offsets = [45, 125]
            x = matches[1][0] + offsets[0]
            y = matches[0][0] + offsets[1]

            self.controller.move_mouse(x, y)
            time.sleep(0.250)
            self.controller.left_mouse_click()
            time.sleep(0.5)

        self.vision.refresh_frame()

    def replace_rune(self, rune_id):
        if rune_id == self.consts._rune_id_Body:
            self.log(f'Replacing Body rune')
            pyautogui.press('f5')
            return True
        elif rune_id == self.consts._rune_id_Malenox:
            self.log(f'Replacing Malenox rune')
            pyautogui.press('f6')
            return True
        elif rune_id == self.consts._rune_id_Agon:
            self.log(f'Replacing Agon rune')
            pyautogui.press('f7')
            return True
        elif rune_id == self.consts._rune_id_Malith:
            self.log(f'Replacing Malith rune')
            pyautogui.press('f8')
            return True
        elif rune_id == self.consts._rune_id_Ulthien:
            self.log(f'Replacing Ulthien rune')
            pyautogui.press('f9')
            return True
        elif rune_id == self.consts._rune_id_Sabal:
            self.log(f'Replacing Sabal rune')
            pyautogui.press('f10')
            return True
        elif rune_id == self.consts._rune_id_Isos:
            self.log(f'Replacing Isos rune')
            pyautogui.press('f11')
            return True
        elif rune_id == self.consts._rune_id_Veldan:
            self.log(f'Replacing Veldan rune')
            pyautogui.press('f12')
            return True
        return False

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.state == 'started':
                healthPercentage = shared.GetMissingHealthPercentage()
                self.log(f'Health: {healthPercentage}%')
                if healthPercentage < 40:
                    self.memory.SetHotbar(8)
                    pyautogui.press('f4')
                elif healthPercentage < 65:
                    self.memory.SetHotbar(8)
                    if self.memory.GetSpell() != self.consts._spell_superior:
                        pyautogui.press('f2')
                    if self.found_self():
                        self.log('Casting heal on self')
                        self.click_self()
                        time.sleep(self.consts._timer_spell_superior)
                if self.state != 'paused': self.state = 'check_stamina'
            elif self.state == 'check_stamina':
                ownStamina = self.memory.GetStamina()
                self.log(f'Stamina: {ownStamina}')
                if ownStamina < 40:
                    self.memory.SetHotbar(8)
                    pyautogui.press('f3')
                if self.state != 'paused': self.state = 'check_party_member'
            elif self.state == 'check_party_member':
                if self.found_party_member():
                    self.memory.SetHotbar(8)
                    if self.memory.GetSpell() != self.consts._spell_superior:
                        pyautogui.press('f2')
                    self.log('Casting heal on party member')
                    self.click_party_member()
                    time.sleep(self.consts._timer_spell_superior)
                if self.state != 'paused': self.state = 'check_runes'
            elif self.state == 'heal_party_member':
                if self.found_party_member():
                    self.memory.SetHotbar(8)
                    if self.memory.GetSpell() != self.consts._spell_superior:
                        pyautogui.press('f2')
                    self.log('Casting heal on party member')
                    self.click_party_member()
                    time.sleep(self.consts._timer_spell_superior)
                if self.state != 'paused': self.state = 'check_runes'
            elif self.state == 'check_runes':
                rune_slots = self.memory.GetRuneSlots()
                rune_types = self.memory.GetRuneTypes()
                rune_charges = self.memory.GetRuneCharges()
                if rune_slots > 0:                    
                    self.log('Checking rune charges...')
                    self.memory.SetHotbar(8)
                    pyautogui.keyDown('shift')
                    time.sleep(0.250)
                    for index in range(rune_slots -1):
                        if self.state == 'paused': break

                        charges = rune_charges[index]
                        time.sleep(0.100)
                        if charges > 0 and charges <= 15:
                            self.replace_rune(rune_types[index])
                            time.sleep(0.250)
                    pyautogui.keyUp('shift')
                    time.sleep(0.250)
                if self.state != 'paused': self.state = 'started'
            else:
                if self.state != 'paused' and self.state != 'not started':
                    self.log('Waiting...')
            time.sleep(0.250)