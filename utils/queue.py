
import traceback
import time
import threading
from collections import deque

import utils.logic as logic


class LoggerThread(threading.Thread):
    _q = deque([], 55)
    processing = False

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(LoggerThread, self).__init__()
        self.target = target
        if name != None:
            self.name = name
        else:
            self.name = 'LoggerThread'
        self._q = deque([], maxlen=55)

        return

    def run(self):
        while True:
            try:
                if len(self._q) > 0:
                    item = self._q.popleft()
                    print('(%s) %s' % (time.strftime('%H:%M:%S'), item))
                else:
                    time.sleep(0.250)
            except Exception as err:
                self.add(f'[{self.name}] {traceback.format_exc()}')

    def add(self, text: str):
        if not text in self._q:
            self._q.append(text)


class ConsumerThread(threading.Thread):
    bot = None
    _q = deque([], maxlen=55)
    processing = False

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        if name != None:
            self.name = name
        else:
            self.name = 'ConsumerThread'
        self.bot = kwargs['bot']
        _maxlen = 55
        if 'max' in kwargs:
            _maxlen = int(kwargs['max'])
        self._q = deque([], maxlen=_maxlen)
        self.processing = False

        return

    def run(self):
        while not self.bot.state == 'shutdown':
            try:
                if len(self._q) > 0 and not self.bot.state == 0 and not self.processing:
                    item = self._q.popleft()
                    self._process(item)
                else:
                    time.sleep(0.250)
            except Exception as err:
                self.bot.log(f'[{self.name}] {traceback.format_exc()}')

    def add(self, name: str = '', addToStart: bool = False):
        if self.bot.state == 0 or self.bot.state == 'shutdown' or name == '':
            return

        if not name in self._q:
            if addToStart:
                self.bot.log(f'[{self.name}] added to start: {name}')
                self._q.appendleft(name)
            else:
                self.bot.log(f'[{self.name}] added: {name}')
                self._q.append(name)

    def _process(self, name: str = ''):
        self.processing = True
        self.bot.log(f'[{self.name}] processing: {name}')
        if name == 'useHealingPotion':
            logic.useHealingPotion()
        elif name == 'useHealingSpell':
            logic.useHealingSpell(self.bot)
        elif name == 'useCallOfTheGodsSpell':
            logic.useCallOfTheGodsSpell(self.bot)
        elif name == 'useStaminaPotion':
            logic.useStaminaPotion()
        elif name == 'getEntitiesOnScreen':
            logic.getEntitiesOnScreen(self.bot)
        elif name == 'getEntityToHeal':
            logic.getEntityToHeal(self.bot)
        elif name == 'getNewTarget':
            logic.getNewTarget(self.bot)
        elif name == 'healSelectedEntity':
            logic.healSelectedEntity(self.bot)
        elif name == 'buffSelectedEntity':
            logic.buffSelectedEntity(self.bot)
        elif name == 'useFood':
            logic.useFood()
        elif name == 'useRegenerationTotem':
            logic.useRegenerationTotem()
        elif name == 'useClassTotem':
            logic.useClassTotem()
        elif name == 'useWerewolfTotem':
            logic.useWerewolfTotem()
        elif name == 'checkRunes':
            logic.checkRunes(self.bot)
        else:
            self.bot.log(f'[{self.name}] Unknown item: {name}')
        self.processing = False
