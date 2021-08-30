
import traceback
import time
import threading
from collections import deque

import utils.logic as logic


class ConsumerThread(threading.Thread):
    bot = None
    _q = deque([], 55)
    processing = False

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.bot = kwargs['bot']
        self._q = deque([], 55)
        self.processing = False

        return

    def run(self):
        while not self.bot.state == 'shutdown':
            try:
                if len(self._q) > 0 and not self.bot.state == 'paused' and not self.processing:
                    item = self._q.popleft()
                    self._process(item)
                else: time.sleep(0.250)
            except Exception as err:
                self.bot.log(f'[ConsumerQ] {traceback.format_exc()}')

    def add(self, name):
        if self.bot.state == 'paused' or self.bot.state == 'shutdown':
            return

        if not name in self._q:
            self.bot.log(f'[ConsumerQ] added: {name}')
            self._q.append(name)

    def _process(self, name=''):
        self.processing = True
        self.bot.log(f'[ConsumerQ] processing: {name}')
        if name == 'useHealingPotion':
            logic.useHealingPotion(self.bot)
        elif name == 'useHealingSpell':
            logic.useHealingSpell(self.bot)
        elif name == 'useCallOfTheGodsSpell':
            logic.useCallOfTheGodsSpell(self.bot)
        elif name == 'useStaminaPotion':
            logic.useStaminaPotion(self.bot)
        elif name == 'getPartyMembersData':
            logic.getPartyMembersData(self.bot)
        elif name == 'updatePartyMembersData':
            logic.updatePartyMembersData(self.bot)
        elif name == 'getPartyMemberToHeal':
            logic.getPartyMemberToHeal(self.bot)
        elif name == 'getPartyOnScreen':
            logic.getPartyOnScreen(self.bot)
        elif name == 'useFood':
            logic.useFood(self.bot)
        elif name == 'useRegenerationTotem':
            logic.useRegenerationTotem(self.bot)
        elif name == 'useClassTotem':
            logic.useClassTotem(self.bot)
        elif name == 'useWerewolfTotem':
            logic.useWerewolfTotem(self.bot)
        elif name == 'checkRunes':
            logic.checkRunes(self.bot)
        else:
            self.bot.log(f'[ConsumerQ] Unknown item: {name}')
        self.processing = False
