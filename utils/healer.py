import time
import keyboard
import threading

import utils.ocr as OCR
import utils.logic as logic
from utils.queue import LoggerThread, ConsumerThread


class HealerThread(threading.Thread):
    state: str = 0
    ocr = OCR
    vision = None
    controller = None
    loggerQ: LoggerThread = None
    workerQ: ConsumerThread = None
    partyQ: ConsumerThread = None
    entityQ: ConsumerThread = None
    process_found: bool = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    party_member_ids = []
    entities_on_screen = []
    party_members_on_screen = []

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(HealerThread, self).__init__()
        self.target = target
        self.name = name
        self.state = 0
        self.ocr = OCR
        self.vision = kwargs['vision']
        self.controller = kwargs['controller']
        self.loggerQ = LoggerThread()
        self.loggerQ.setDaemon(True)
        self.loggerQ.start()
        self.workerQ = ConsumerThread(kwargs={'bot': self})
        self.workerQ.setDaemon(True)
        self.workerQ.start()
        self.partyQ = ConsumerThread(kwargs={'bot': self})
        self.partyQ.setDaemon(True)
        self.partyQ.start()
        self.entityQ = ConsumerThread(kwargs={'bot': self})
        self.entityQ.setDaemon(True)
        self.entityQ.start()
        self.process_found = False
        self.usedSpell = False
        self.cog_timeout = False
        self.last_poison_disease = 0
        self.last_party_count = 0
        self.party_member_ids = []
        self.entities_on_screen = []
        self.party_members_on_screen = []

        keyboard.add_hotkey('pause', self.toggle_pause)
        keyboard.add_hotkey('ctrl+n', self.checkMouseNPCId)

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
        with self.memory.GameProcess() as process:
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
            newPoisonDisease = self.memory.GetPoisonDisease()
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
        ownStamina = self.memory.GetStamina()
        if ownStamina < 100:
            self.log(f'[Healer] Stamina: {ownStamina}')

        if ownStamina < 40:
            self.workerQ.add('useStaminaPotion')

    def checkPartyData(self):
        partyCount = self.memory.GetPartyCount()
        # Party count changed, update count and take new images
        if partyCount != self.last_party_count:
            self.log(f'[Healer] Party Member Count: [{partyCount}]')
            self.last_party_count = partyCount
            self.partyQ.add('getPartyMembersIds')
        else:
            self.partyQ.add('getPartyMembersOnScreen')

    def checkPartyHeals(self):
        if self.memory.GetPartyCount() > 1:
            self.workerQ.add('getPartyMemberToHeal')

    def checkEntitiesOnScreen(self):
        self.entityQ.add('getEntitiesOnScreen')

    def checkMouseNPCId(self):
        npcID = self.memory.GetMouseNPCId()
        self.log(f'[Healer] GetMouseNPCId: {npcID}')

    def checkSystemMessage(self):
        message = self.memory.CheckSystemMessage()
        if message != '' and message != 0:
            self.log(f'[Healer] CheckSystemMessage: {message}')

    def checkGuildMessage(self):
        message = self.memory.GetGuildMessage()
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
                    threading.Thread(target=self.checkEntitiesOnScreen).start()
                    if (_tick % 2) == 0:
                        threading.Thread(target=self.checkPartyHeals).start()
                    else:
                        threading.Thread(target=self.checkPartyData).start()

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
