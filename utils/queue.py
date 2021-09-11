
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

    def add(self, text: str):
        if not text in self._q:
            self._q.append(text)

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

    def _process(self, name: str = ''):
        self.processing = True
        self.bot.log(f'[{self.name}] processing: {name}')
        if name == 'use_healing_potion':
            logic.use_healing_potion()
        elif name == 'use_healing_spell':
            logic.use_healing_spell(self.bot)
        elif name == 'use_call_of_the_gods_spell':
            logic.use_call_of_the_gods_spell(self.bot)
        elif name == 'use_stamina_potion':
            logic.use_stamina_potion()
        elif name == 'get_entities_on_screen':
            logic.get_entities_on_screen(self.bot)
        elif name == 'get_entity_to_heal':
            logic.get_entity_to_heal(self.bot)
        elif name == 'target_new_enemy':
            logic.target_new_enemy(self.bot)
        elif name == 'heal_selected_entity':
            logic.heal_selected_entity(self.bot)
        elif name == 'buff_selected_entity':
            logic.buff_selected_entity(self.bot)
        elif name == 'use_food':
            logic.use_food()
        elif name == 'use_regeneration_totem':
            logic.use_regeneration_totem()
        elif name == 'use_class_totem':
            logic.use_class_totem()
        elif name == 'use_werewolf_totem':
            logic.use_werewolf_totem()
        elif name == 'check_runes':
            logic.check_runes(self.bot)
        else:
            self.bot.log(f'[{self.name}] Unknown item: {name}')
        self.processing = False

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
