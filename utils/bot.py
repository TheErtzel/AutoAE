import time
import keyboard
import threading

import utils.logic as logic
from utils.queue import ConsumerThread


class BotThread(threading.Thread):
    state = 'paused'
    consts = None
    memory = None
    ocr = None
    vision = None
    controller = None
    queue = None
    process_found = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    party_member_data = []

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BotThread, self).__init__()
        self.target = target
        self.name = name
        self.state = 'paused'
        self.consts = kwargs['consts']
        self.memory = kwargs['memory']
        self.ocr = kwargs['ocr']
        self.vision = kwargs['vision']
        self.controller = kwargs['controller']
        self.queue = ConsumerThread(kwargs={'bot': self})
        self.queue.setDaemon(True)
        self.queue.start()
        self.process_found = False
        self.usedSpell = False
        self.cog_timeout = False
        self.last_poison_disease = 0
        self.last_party_count = 0
        self.party_member_data = []
        self.party_members_on_screen = []

        keyboard.add_hotkey('pause', self.toggle_pause)

    def log(self, text):
        print('(%s) %s' % (time.strftime('%H:%M:%S'), text))

    def setState(self, state):
        if not self.state == 'paused':
            self.state = state

    def toggle_pause(self):
        if self.state == 'paused':
            self.state = 'running'
            self.log('Un-paused')
        else:
            self.state = 'paused'
            self.log('Paused')
        time.sleep(0.500)

    def checkGame(self):
        with self.memory.GameProcess() as process:
            if self.process_found == True and process == None:
                self.process_found = False
            elif self.process_found == False and process != None:
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
        if healthPercentage < 100:
            self.log(f'Health: {healthPercentage}%')

        if healthPercentage < 98:
            newPoisonDisease = self.memory.GetPoisonDisease()
            if newPoisonDisease != self.last_poison_disease:
                self.last_poison_disease = newPoisonDisease
                if newPoisonDisease > 0:  # Check if we are now poisoned or diseased
                    self.log('PoisonDisease: {bot.last_poison_disease}')
                    if self.cog_timeout == False:  # Check if we aren't waiting on cog cooldown
                        self.queue.add('useCallOfTheGodsSpell')
                        return

        if healthPercentage < 35:
            self.queue.add('useHealingPotion')
        elif healthPercentage < 65:
            self.queue.add('useHealingSpell')

    def checkOwnStamina(self):
        ownStamina = self.memory.GetStamina()
        if ownStamina < 100:
            self.log(f'Stamina: {ownStamina}')

        if ownStamina < 40:
            self.queue.add('useStaminaPotion')

    def checkPartyWindow(self):
        partyCount = self.memory.GetPartyCount()
        # Party count changed, update count and take new images
        if partyCount != self.last_party_count:
            self.log(f'[Logic] Party Member Count: [{partyCount}]')
            self.last_party_count = partyCount
            time.sleep(0.250)
            self.queue.add('updatePartyMemberData')
        self.queue.add('updatePartyMemberHealths')

    def checkParty(self):
        partyCount = self.memory.GetPartyCount()
        # Party count changed, update count and take new images
        if partyCount != self.last_party_count:
            self.log(f'[Logic] Party Member Count: [{partyCount}]')
            self.last_party_count = partyCount
            time.sleep(0.250)
            self.queue.add('updatePartyMemberData')
        self.queue.add('updatePartyMemberHealths')

        if partyCount > 1:
            self.queue.add('getPartyMemberToHeal')

    def checkTotemsAndFood(self):
        chatLogs = logic.getLastChannelLogs('System', 10)
        if 'The effect from your food has faded' in chatLogs:
            self.queue.add('useFood')
        if 'Your added health has faded' in chatLogs:
            self.queue.add('useRegenerationTotem')
        elif 'Your added stamina has faded' in chatLogs:
            self.queue.add('useRegenerationTotem')
        if 'Your added strength has faded' in chatLogs:
            self.queue.add('useClassTotem')
        elif 'Your added dexterity has faded' in chatLogs:
            self.queue.add('useClassTotem')
        elif 'Your added intelligence has faded' in chatLogs:
            self.queue.add('useClassTotem')
        elif 'Your added constitution  has faded' in chatLogs:
            self.queue.add('useClassTotem')
        if 'Your attack speed returns to normal' in chatLogs:
            self.queue.add('useWerewolfTotem')

    def run(self):
        self.log('[Bot] Started! press [pause] to toggle pause/un-pause')

        while True:
            if self.state == 'running':
                self.checkGame()
                if self.process_found:
                    threading.Thread(target=self.checkOwnHealth).start()
                    threading.Thread(target=self.checkOwnStamina).start()
                    threading.Thread(target=self.checkParty).start()
                    threading.Thread(target=self.checkTotemsAndFood).start()
                else:
                    self.log('[Bot] Game Process not found!')
                    self.log('[Bot] Waiting...')
                    time.sleep(30)
            time.sleep(0.5)
