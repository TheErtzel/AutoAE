import time
import keyboard
import threading

import utils.constants as consts
import utils.memory as memory
import utils.logic as logic
from utils.queue import LoggerThread, ConsumerThread


class HealerThread(threading.Thread):
    state: str = 0
    controller = None
    loggerQ: LoggerThread = None
    workerQ: ConsumerThread = None
    backgroundQ: ConsumerThread = None
    process_found: bool = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    entities_on_screen = []

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(HealerThread, self).__init__()
        self.target = target
        self.name = name
        self.state = 0
        self.controller = kwargs['controller']
        self.loggerQ = LoggerThread()
        self.loggerQ.setDaemon(True)
        self.loggerQ.start()
        self.workerQ = ConsumerThread(kwargs={'bot': self})
        self.workerQ.setDaemon(True)
        self.workerQ.start()
        self.backgroundQ = ConsumerThread(kwargs={'bot': self})
        self.backgroundQ.setDaemon(True)
        self.backgroundQ.start()
        self.process_found = False
        self.usedSpell = False
        self.cog_timeout = False
        self.last_poison_disease = 0
        self.entities_on_screen = []

        keyboard.add_hotkey('pause', self.toggle_pause)
        keyboard.add_hotkey('ctrl+n', self.checkMouseId)
        keyboard.add_hotkey('ctrl+insert', self.entityData)

    def log(self, text):
        self.loggerQ.add(text)

    def setState(self, state):
        if not self.state == 0:
            self.state = state

    def toggle_pause(self):
        if self.state == 0:
            self.state = 1
            self.log('[Healer] Un-paused')
        else:
            self.state = 0
            self.log('[Healer] Paused')
        time.sleep(0.500)

    def checkGame(self):
        with memory.GameProcess() as process:
            if process == None:
                self.process_found = False
            else:
                self.process_found = True

    def callOfTheGodsTimeout(self):
        tick = 12
        self.cog_timeout = True
        while tick > 0 and self.is_paused == False:
            time.sleep(1)
            tick -= 1
        self.cog_timeout = False

    def checkOwnHealth(self):
        healthPercentage = logic.getMissingHealthPercentage()
        if healthPercentage < 100:
            self.log(f'[Healer] Health: {healthPercentage}%')

        if healthPercentage < 98:
            newPoisonDisease = memory.GetPoisonDisease()
            if newPoisonDisease != self.last_poison_disease:
                self.last_poison_disease = newPoisonDisease
                if newPoisonDisease > 0:  # Check if we are now poisoned or diseased
                    self.log('PoisonDisease: {bot.last_poison_disease}')
                    if self.cog_timeout == False:  # Check if we aren't waiting on cog cooldown
                        self.workerQ.add('useCallOfTheGodsSpell')
                        return

        if healthPercentage < 35:
            self.workerQ.add('useHealingPotion')
        elif healthPercentage < 80:
            self.workerQ.add('useHealingSpell')

    def checkOwnStamina(self):
        ownStamina = memory.GetStamina()
        if ownStamina < 100:
            self.log(f'[Healer] Stamina: {ownStamina}')

        if ownStamina < 40:
            self.workerQ.add('useStaminaPotion')

    def checkEntitiesOnScreen(self):
        self.backgroundQ.add('getEntitiesOnScreen')

    def checkEntityToHeal(self):
        if len(self.entities_on_screen) > 0:
            self.workerQ.add('getEntityToHeal')

    def checkMouseId(self):
        id = memory.GetMouseId()
        self.log(f'[Healer] GetMouseId: {id}')

    def entityData(self):
        entities = []
        selfLoc = memory.GetLocation()
        offset = consts.SCREEN_HEX[0]
        self.log(f'[Attacker] Getting entities on screen...')
        while offset < consts.SCREEN_HEX[1]:
            entity = memory.GetEntityData(offset)
            if entity['id'] != 0 and entity['name'] != '':
                distance = logic.getDistanceApart(selfLoc, entity['coords'])
                if distance[0] <= 14 and distance[0] >= -13 and distance[1] <= 12 and distance[1] >= -12:
                    entity['distance'] = distance
                    entity['percentage'] = logic.getMissingHealthPercentage(
                        entity['hp'][0], entity['hp'][1])
                    entities.append(entity)
            offset += 4
        entities = logic.sortBy(logic.filter(
            entities, 'name'), 'percentage', True)
        self.log(
            f'[Attacker] GetEntityNames: {entities}')
        self.log(
            f'[Attacker] GetEntityPercentages: {logic.flatten(entities, "percentage")}')

        self.log(f'[Attacker] (2) Getting entities on screen...')
        for offset in consts.SCREEN_ENTITY_OFFSETS:
            for i in range(1):
                hexCode = hex(offset + (i * 4))
                entity = memory.GetEntityData(hexCode)
                if entity['id'] != 0 and entity['name'] != '':
                    distance = logic.getDistanceApart(
                        selfLoc, entity['coords'])
                    if distance[0] <= 14 and distance[0] >= -13 and distance[1] <= 12 and distance[1] >= -12:
                        entity['distance'] = distance
                        entity['percentage'] = logic.getMissingHealthPercentage(
                            entity['hp'][0], entity['hp'][1])
                        entities.append(entity)
        entities = logic.sortBy(logic.filter(
            entities, 'name'), 'percentage', True)
        self.log(
            f'[Attacker] (2) GetEntityNames: {logic.flatten(entities, "name")}')
        self.log(
            f'[Attacker] (2) GetEntityPercentages: {logic.flatten(entities, "percentage")}')

    def checkSystemMessage(self):
        message = memory.CheckSystemMessage()
        if message != '' and message != 0:
            self.log(f'[Healer] CheckSystemMessage: {message}')

    def checkGuildMessage(self):
        message = memory.GetGuildMessage()
        if message != '' and message != 0:
            self.log(f'[Healer] GetGuildMessage: {message}')

    def checkTotemsAndFood(self):
        chatLogs = logic.getLastChannelLogs('Say', 10)

        if logic.checkLogsForMessage(chatLogs, 'The effect from your food has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Eating the food'):
            self.workerQ.add('useFood')
        if logic.checkLogsForMessage(chatLogs, 'Your added health regen has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your health and stamina regen increase'):
            self.workerQ.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added stamina regen has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your health and stamina regen increase'):
            self.workerQ.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added strength has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added strength'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added dexterity has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added dexterity'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added intelligence has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added intelligence'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added constitution has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added constitution'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your attack speed returns to normal') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your attack speed has been increased'):
            self.workerQ.add('useWerewolfTotem')

    def run(self):
        self.log('[Healer] Started! press [pause] to toggle pause/un-pause')
        _tick = 0

        while True:
            if self.state == 1:
                self.checkGame()
                if self.process_found:
                    _tick += 1
                    threading.Thread(target=self.checkSystemMessage).start()
                    # threading.Thread(target=self.checkGuildMessage).start()
                    if (_tick % 2) == 0:
                        threading.Thread(
                            target=self.checkEntitiesOnScreen).start()
                    else:
                        threading.Thread(target=self.checkEntityToHeal).start()

                    if _tick == 10:
                        threading.Thread(target=self.checkOwnHealth).start()
                        threading.Thread(target=self.checkOwnStamina).start()
                    elif _tick > 20:
                        # threading.Thread(
                        #    target=self.checkTotemsAndFood).start()
                        _tick = 0
                else:
                    self.log('[Healer] Game Process not found!')
                    self.log('[Healer] Waiting...')
                    time.sleep(30)
            time.sleep(0.250)
