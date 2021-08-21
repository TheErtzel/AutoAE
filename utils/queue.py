
import traceback
import time
import threading
from collections import deque

import utils.logic as logic


class ConsumerThread(threading.Thread):
    bot = None
    workerQ = deque([], 55)
    processing = False

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.bot = kwargs['bot']
        self.workerQ = deque([], 55)
        self.processing = False

        return

    def run(self):
        while not self.bot.state == 'shutdown':
            try:
                if len(self.workerQ) > 0 and not self.bot.state == 'paused' and not self.processing:
                    item = self.workerQ.popleft()
                    self._process(item)
                time.sleep(1)
            except Exception as err:
                self.bot.log(f'[Consumer] {traceback.format_exc()}')

    def add(self, name):
        if self.bot.state == 'paused' or self.bot.state == 'shutdown':
            return

        if not name in self.workerQ:
            self.bot.log(f'[Consumer] added: {name}')
            self.workerQ.append(name)

    def _process(self, name=''):
        self.processing = True
        self.bot.log(f'[Consumer] processing: {name}')
        if name == 'useHealingPotion':
            logic.useHealingPotion(self.bot)
        elif name == 'useHealingSpell':
            logic.useHealingSpell(self.bot)
        elif name == 'useCallOfTheGodsSpell':
            logic.useCallOfTheGodsSpell(self.bot)
        elif name == 'useStaminaPotion':
            logic.useStaminaPotion(self.bot)
        elif name == 'updatePartyMemberData':
            logic.updatePartyMemberData(self.bot)
        elif name == 'updatePartyMemberHealths':
            logic.updatePartyMemberHealths(self.bot)
        elif name == 'getPartyMemberToHeal':
            logic.getPartyMemberToHeal(self.bot)
        elif name == 'checkRunes':
            logic.checkRunes(self.bot)
        else:
            self.bot.log(f'[Consumer] Unknown item: {name}')
        self.processing = False
