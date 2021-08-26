import time
import keyboard
import threading

import utils.logic as logic
from utils.queue import ConsumerThread


class BotThread(threading.Thread):
    state: str = 'paused'
    consts = None
    memory = None
    ocr = None
    vision = None
    controller = None
    queue: ConsumerThread = None
    process_found: bool = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    party_members_data = []
    party_members_on_screen = []
    active_party_member_name: str = ''

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
        self.party_members_data = []
        self.party_members_on_screen = []
        self.active_party_member_name = ''

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
        elif healthPercentage < 80:
            self.queue.add('useHealingSpell')

    def checkOwnStamina(self):
        ownStamina = self.memory.GetStamina()
        if ownStamina < 100:
            self.log(f'Stamina: {ownStamina}')

        if ownStamina < 40:
            self.queue.add('useStaminaPotion')

    def checkPartyData(self):
        partyCount = self.memory.GetPartyCount()
        # Party count changed, update count and take new images
        if partyCount != self.last_party_count:
            self.log(f'[Logic] Party Member Count: [{partyCount}]')
            self.last_party_count = partyCount
            time.sleep(0.250)
            logic.updatePartyMembersData(self)
        else:
            logic.updatePartyMembersHealth(self)

    def checkPartyHeals(self):
        if self.memory.GetPartyCount() > 1:
            self.queue.add('getPartyMemberToHeal')

    def checkMouse(self):
        if self.memory.GetPartyCount() > 1:
            self.queue.add('getPartyOnScreen')

    def checkTotemsAndFood(self):
        chatLogs = logic.getLastChannelLogs('Say', 10)

        if logic.checkLogsForMessage(chatLogs, 'The effect from your food has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Eating the food'):
            self.queue.add('useFood')
        if logic.checkLogsForMessage(chatLogs, 'Your added health regen has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your health and stamina regen increase'):
            self.queue.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added stamina regen has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your health and stamina regen increase'):
            self.queue.add('useRegenerationTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added strength has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added strength'):
            self.queue.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added dexterity has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added dexterity'):
            self.queue.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added intelligence has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added intelligence'):
            self.queue.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your added constitution has faded') and not logic.checkLogsForMessage(chatLogs[-5:], 'You feel added constitution'):
            self.queue.add('useClassTotem')
        if logic.checkLogsForMessage(chatLogs, 'Your attack speed returns to normal') and not logic.checkLogsForMessage(chatLogs[-5:], 'Your attack speed has been increased'):
            self.queue.add('useWerewolfTotem')

    def run(self):
        self.log('[Bot] Started! press [pause] to toggle pause/un-pause')
        _tick = 0

        while True:
            if self.state == 'running':
                self.checkGame()
                if self.process_found:
                    _tick += 1
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
                    self.log('[Bot] Game Process not found!')
                    self.log('[Bot] Waiting...')
                    time.sleep(30)
            time.sleep(0.250)


def main():
    from utils.controller import Controller
    from utils.vision import Vision
    import utils.constants as consts
    import utils.memory as memory
    import utils.ocr as ocr

    vision = Vision()
    controller = Controller()
    bot = BotThread(kwargs={'consts': consts, 'memory': memory,
                            'ocr': ocr, 'vision': vision, 'controller': controller})
    bot.start()


if __name__ == '__main__':
    main()
