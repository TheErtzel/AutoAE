import time
import keyboard
import threading

import utils.logic as logic
from utils.queue import LoggerThread, ConsumerThread


class AttackerThread(threading.Thread):
    state: str = 0
    consts = None
    memory = None
    ocr = None
    vision = None
    controller = None
    loggerQ: LoggerThread = None
    workerQ: ConsumerThread = None
    process_found: bool = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    looking_for_target: bool = False

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(AttackerThread, self).__init__()
        self.target = target
        self.name = name
        self.state = 0
        self.consts = kwargs['consts']
        self.memory = kwargs['memory']
        self.ocr = kwargs['ocr']
        self.vision = kwargs['vision']
        self.controller = kwargs['controller']
        self.loggerQ = LoggerThread()
        self.loggerQ.setDaemon(True)
        self.loggerQ.start()
        self.workerQ = ConsumerThread(kwargs={'bot': self})
        self.workerQ.setDaemon(True)
        self.workerQ.start()
        self.process_found = False
        self.usedSpell = False
        self.cog_timeout = False
        self.last_poison_disease = 0
        self.looking_for_target = False

        keyboard.add_hotkey('pause', self.toggle_pause)

    def log(self, text):
        self.loggerQ.add(text)

    def setState(self, state):
        if not self.state == 0:
            self.state = state

    def toggle_pause(self):
        if self.state == 0:
            self.state = 1
            self.log('[Attacker] Un-paused')
        else:
            self.state = 0
            self.log('[Attacker] Paused')
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
        healthPercentage = logic.getMissingHealthPercentage(
            self.memory)
        if healthPercentage == 100:
            return

        if healthPercentage < 98:
            newPoisonDisease = self.memory.GetPoisonDisease()
            if newPoisonDisease != self.last_poison_disease:
                self.last_poison_disease = newPoisonDisease
                if newPoisonDisease > 0:  # Check if we are now poisoned or diseased
                    self.log(f'[Attacker] Health: {healthPercentage}%')
                    self.log('PoisonDisease: {bot.last_poison_disease}')
                    if self.cog_timeout == False:  # Check if we aren't waiting on cog cooldown
                        self.workerQ.add('useCallOfTheGodsSpell')
                        return

        if healthPercentage < 35:
            self.log(f'[Attacker] Health: {healthPercentage}%')
            self.workerQ.add('useHealingPotion')
        elif healthPercentage < 65:
            self.log(f'[Attacker] Health: {healthPercentage}%')
            self.workerQ.add('useHealingSpell')

    def checkOwnStamina(self):
        ownStamina = self.memory.GetStamina()

        if ownStamina < 40:
            self.log(f'[Attacker] Stamina: {ownStamina}')
            self.workerQ.add('useStaminaPotion')

    def checkTarget(self):
        target = self.memory.GetTargetId()
        if target == 0:
            self.workerQ.add('getNewTarget')

    def checkSystemMessage(self):
        message = self.memory.CheckSystemMessage()
        if message != '' and message != 0:
            self.log(f'[Attacker] CheckSystemMessage: {message}')

    def checkGuildMessage(self):
        message = self.memory.GetGuildMessage()
        if message != '' and message != 0:
            self.log(f'[Attacker] GetGuildMessage: {message}')

    def checkTotemsAndFood(self):
        chatLogs = logic.getLastChannelLogs('Say', 10)

        if logic.checkLogsForMessage(chatLogs, 'The effect from your food has faded', 'Eating the food'):
            self.workerQ.add('useFood')
        if logic.checkLogsForMessage(chatLogs, 'Your added health regen has faded', 'Your health and stamina regen increase'):
            self.workerQ.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added stamina regen has faded', 'Your health and stamina regen increase'):
            self.workerQ.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added strength has faded', 'You feel added strength'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added dexterity has faded', 'You feel added dexterity'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added intelligence has faded', 'You feel added intelligence'):
            self.workerQ.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added constitution has faded', 'You feel added constitution'):
            self.workerQ.add('useClassTotem')
        # if logic.checkLogsForMessage(chatLogs, 'Your attack speed returns to normal', 'Your attack speed has been increased'):
        self.workerQ.add('useWerewolfTotem')

    def run(self):
        self.log('[Attacker] Started! press [pause] to toggle pause/un-pause')
        _tick = 0

        while True:
            threading.Thread(target=self.checkSystemMessage).start()
            if self.state == 1:
                self.checkGame()
                if self.process_found:
                    _tick += 1
                    if not self.looking_for_target:
                        threading.Thread(target=self.checkTarget).start()
                    threading.Thread(target=self.checkOwnHealth).start()
                    threading.Thread(target=self.checkOwnStamina).start()
                    if _tick > 20:
                        threading.Thread(
                            target=self.checkTotemsAndFood).start()
                        _tick = 0
                else:
                    self.log('[Attacker] Game Process not found!')
                    self.log('[Attacker] Waiting...')
                    time.sleep(30)
            time.sleep(0.250)