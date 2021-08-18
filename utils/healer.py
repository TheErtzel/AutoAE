import time
from tkinter import *
from ReadWriteMemory import ReadWriteMemory

import utils.constants as consts
import utils.memory as memory
import utils.shared as shared

def RunChecks(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root.is_paused: return

    if not root.is_waiting:
        CheckOwnHealth([root])
        CheckStam([root])
        CheckRunes([root])
        CheckTotems([root])

def CheckStam(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None or root.is_paused == True: return

    stamina_value = memory.GetStamina()
    if stamina_value == 0: return
    elif stamina_value < 35:
        return # Use stamina potion

def CheckRunes(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None or root.is_paused == True: return

    rune_slots = memory.GetRuneSlots()
    if rune_slots > 0:
        rune_types = memory.GetRuneTypes()
        rune_charges = memory.GetRuneCharges()
        for index in range(rune_slots -1):
            charges = rune_charges[index]
            if charges > 0 and charges <= 15: return #replace rune at rune_types[index]


def CheckTotems(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None or root.is_paused == True: return

    stamRegen = memory.GetStaminaRegen()
    if stamRegen == 1 or stamRegen == 3 or stamRegen == 5: return
    # use totem of regeneration
    # use class totem
    # use werewolf totem


def CheckBuffs(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None: return

    memory.SetHotbar(2)
    shared.UseHotbarItem([root, 'f2', False])
    tmr = 3000
    
def CheckOwnHealth(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None or root.is_paused == True: return

    newPoisonDisease = memory.GetPoisonDisease()
    if newPoisonDisease != root.last_poison_disease:
        root.last_poison_disease = newPoisonDisease
        if newPoisonDisease > 0: # Check if we are now poisoned or diseased
            root.debug('PoisonDisease: {newPoisonDisease}')
            if root.cog_timeout == False: # Check if we aren't waiting on cog cooldown
                return # queue cog spell
            return

    missing_health_perctnage = shared.GetMissingHealthPercentage()
    if missing_health_perctnage == 0: return
    
    if missing_health_perctnage < 25: # If we are below 25% health, use a potion
        return #queue health potion
    elif missing_health_perctnage < 70: # If we are below 80% health, cast a heal
        return #queue health spell

def CheckPartyHealth(args=()):
    root = None
    if len(args) > 0: root = args[0]
    if root == None or root.is_paused == True: return False

    if not root.is_paused:
        return # Check for who in party needs to be healed