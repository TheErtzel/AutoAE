from ReadWriteMemory import ReadWriteMemory

# Hex Codes
_base = 0x400000 #8/11
_base_self = 0x00351100 #8/11
_base_location = 0x003502D4 #8/12
_base_follower = 0x00350F54 #8/12
_base_party = 0x003B1AB8 #8/13
_base_rune = 0x03B1B44 #8/11
_base_rune_slots = 0x03B1B48 #8/13
_base_hotbar = 0x00351158 #8/12
_base_spell = 0x3B1B48 #8/13
_base_spell_type = 0x003B1A68 #8/13
_x_offset = 0x2F4 #5/11
_y_offset = 0x2F8 #5/11
_screen_width = 0x0048  #8/12
_screen_height = 0x0044 #8/12
_level_offset = 0x444 #8/12
_max_health = 0x29C #8/11
_cur_health = 0x298 #8/11
_stamina = 0x4A4 #8/11
_stamina_regen = 0x578 #8/12
_armor = 0x2D0 #8/12
_weight = 0x2A0 #8/12
_target_offset = 0x5F4 #8/12
_follower_mode_offset = 0x48 #8/12
_follower_hp_offset = 0x4C #8/12
_follower_hp_max_offset = 0x50 #8/12
_can_move_offset = 0x678 #8/14
_party_count_offset = 0x138 #8/13
_hotbar_offset = 0x4 #8/12
_poison_disease_offset = 0x580 #8/13
_spell_offset = 0x10808 #8/13
_spell_type_offset = 0x50 #8/13
_spell_state_offset = 0x5F0 #8/11
_rune_type_offset = 0x10818 #8/15
_rune_charge_offset = 0x10840 #8/13
_rune_slots_offset = 0x10810 #8/13

class GameProcess():
    rmw = None
    process = None
    def __init__(self):
        try:
            self.rmw = ReadWriteMemory()
            self.process = self.rmw.get_process_by_name("client.exe")
        except Exception as err:
            self.rmw = None
            self.process = None
    def __enter__(self):
        if self.process != None: self.process.open()
        return self.process
    def __exit__(self, type, value, traceback):
        if self.process != None:
            self.process.close()

def SetHotbar(number):
    if not isinstance(number, (int, float)): number = number[0]
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
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_hotbar, offsets=[_hotbar_offset])
            result = process.write(point, towrite)
    return result

def SetSpell(number):
    if not isinstance(number, (int, float)): number = number[0]
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_spell , offsets=[_spell_offset])
            result = process.write(point, number)
    return result

def SetSpellState(number):
    if not isinstance(number, (int, float)): number = number[0]
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_spell_state_offset])
            result = process.write(point, number)
    return result

def SetSpellType(number):
    # 0 = none, 2 = combat, 3 = heal, 5 = buff?,  8 = res?, 16 = AoE combat, 17 = AoE heal
    if not isinstance(number, (int, float)): number = number[0]
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_spell_type , offsets=[_spell_type_offset])
            result = process.write(point, number)
    return result

def GetProgramWidth():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_screen_width])
            result = process.read(point)
    return result

def GetProgramHeight():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_screen_height])
            result = process.read(point)
    return result

def GetY():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_location, offsets=[_y_offset])
            result = process.read(point)
    return result

def GetX():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_location, offsets=[_x_offset])
            result = process.read(point)
    return result

def GetMouseX():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0680])
            result = process.read(point)
    return result

def GetMouseY():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0684])
            result = process.read(point)
    return result

def GetMouseClick():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x0678])
            result = process.read(point)
    return result

def GetMouseNPCId():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[0x05F8])
            result = process.read(point)
    return result

def GetHotbar():
    result = 57
    with GameProcess() as process:  
        if process != None:
            point = process.get_pointer(_base + _base_hotbar, offsets=[_hotbar_offset])
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

def GetSpell():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_spell , offsets=[_spell_offset])
            result = process.read(point)
    return result

def GetSpellState():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_spell_state_offset])
            result = process.read(point)
    return result

def GetSpellType():
    # 0 = none, 2 = combat, 3 = heal, 5 = buff?,  8 = res?, 16 = AoE combat, 17 = AoE heal
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_spell_type , offsets=[_spell_type_offset])
            result = process.read(point)
    return result

def GetRuneTypes():
    runelist = []
    typeOffset = _rune_type_offset
    with GameProcess() as process:
        if process != None:
            for x in range(9):
                point = process.get_pointer(_base + _base_spell, offsets=[typeOffset])
                result = process.read(point)
                runelist.append(result)
                typeOffset = typeOffset + 4
    return runelist

def GetRuneCharges():
    chargeOffset = _rune_charge_offset
    chargelist = []
    with GameProcess() as process:
        if process != None:
            for x in range(9):
                point = process.get_pointer(_base + _base_spell, offsets=[chargeOffset])
                result = process.read(point)
                chargelist.append(result)
                chargeOffset = chargeOffset + 4
    return chargelist

def GetRuneSlots():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_spell, offsets=[_rune_slots_offset])
            result = process.read(point)
    return result

def GetCanMove(): 
    # returns 1 if you can move, 0 if not.
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self , offsets=[_can_move_offset])
            result = process.read(point)
    return result == 1

def CurrentLevel():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_level_offset])
            result = process.read(point)
    return result

def GetPoisonDisease():
    #returns 4294967295 or -1 for none, 256 for disease, 1 for poison
    result = -1
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_poison_disease_offset])
            result = process.read(point)
            if result == 4294967295: result = 0
    return result

def GetArmor():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_armor])
            result = process.read(point)
    return result

def GetCurWeight():
    result = 0
    with GameProcess() as process:  
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_weight])
            num = process.read(point)
            result = num
            if num > 0: 
                result = int(str(num)[:-2]) # convert to a string to remove the last 2 numbers then convert back to an int
    return result

def GetStaminaRegen():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_stamina_regen])
            result = process.read(point)
    return result

def GetStamina():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_stamina])
            result = process.read(point)
    return result

def GetMaxHealth():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self , offsets=[_max_health])
            result = process.read(point)
    return result

def GetCurHealth():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_self, offsets=[_cur_health])
            result = process.read(point)
    return result

def GetPartyCount():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_party, offsets=[_party_count_offset])
            result = process.read(point)
    return result

def GetTargetId():
    # returns 0 if no target is selected, and the target id if it is.
    result = 0
    with GameProcess() as process:
        point = process.get_pointer(_base + _base_self, offsets=[_target_offset])
        result = process.read(point)
    return result    

def CheckFollower():
    # 0 = None, 11 = Follow, 12 = Stay, 13 = Protect, 15 = Guard, 16 = Attack, 17 = Inv, 18 = Flee, 19 = Assist
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_follower, offsets=[_follower_mode_offset])
            result = process.read(point)
    return result

def GetFollowerMaxHealth():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_follower , offsets=[_follower_hp_max_offset])
            result = process.read(point)
    return result

def GetFollowerHealth():
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + _base_follower, offsets=[_follower_hp_offset])
            result = process.read(point)
    return result    

def CheckSystemMessage(): 
    # returns 0 if no msg, and a value if message is present on screen
    # 15139368 = PrivateMessage?
    result = 0
    with GameProcess() as process:
        if process != None:
            point = process.get_pointer(_base + 0x003B1B50)
            result = process.read(point)
    return result