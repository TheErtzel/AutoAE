import time
import keyboard
import threading

from utils.bot import BotThread
from utils.queue import LoggerThread, ConsumerThread


class HealerThread(BotThread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super().__init__(name)
        self.state = 0
        self.logger_queue = LoggerThread(name='LoggerQueue')
        self.logger_queue.setDaemon(True)
        self.logger_queue.start()
        self.worker_queue = ConsumerThread(
            name='WorkerQueue', kwargs={'bot': self})
        self.worker_queue.setDaemon(True)
        self.worker_queue.start()
        self.background_queue = ConsumerThread(
            name='BackgroundQueue', kwargs={'bot': self, 'max': 10})
        self.background_queue.setDaemon(True)
        self.background_queue.start()
        self.process_found = False
        self.usedSpell = False
        self.cog_timeout = False
        self.last_poison_disease = 0
        self.looking_for_target = False
        self.entities_on_screen = []
        self.non_player_ids = []
        self.selected_entity = None
        self.ignored_ids = []

        keyboard.add_hotkey('pause', self.toggle_pause)

        keyboard.add_hotkey('ctrl+n', self.check_mouse_id)
        keyboard.add_hotkey('ctrl+insert', self.entity_data)
        keyboard.add_hotkey('delete', self.buff_mouse_entity)
        keyboard.add_hotkey('end', self.select_heal)
        keyboard.add_hotkey('ctrl+alt', self.get_selected_entity)

        keyboard.add_hotkey('ctrl+-', self.toggle_none)
        keyboard.add_hotkey('ctrl+/', self.toggle_auto)
        keyboard.add_hotkey('ctrl+*', self.toggle_buff)

    def check_entities_on_screen(self) -> None:
        if self.state < 2:
            return

        self.background_queue.add('get_entities_on_screen')

    def check_entity_to_heal(self) -> None:
        if self.state != 2:
            return

        if self.selected_entity == None:
            self.worker_queue.add('get_entity_to_heal')

    def run(self) -> None:
        self.log(
            f'[{self.name}] Started! press [pause] to toggle pause/un-pause')
        _tick = 0

        while True:
            if self.state == 2 or self.state == 3:
                self.check_game()
                if self.process_found:
                    if self.state == 2:
                        _tick += 1
                        # threading.Thread(target=self.check_system_message).start()
                        # threading.Thread(target=self.check_guild_message).start()
                        threading.Thread(
                            target=self.check_totems_and_food).start()

                        if (_tick % 2) == 0:
                            threading.Thread(
                                target=self.check_entities_on_screen).start()
                        else:
                            threading.Thread(
                                target=self.check_entity_to_heal).start()

                        if (_tick % 10) == 0:
                            threading.Thread(
                                target=self.check_own_health).start()
                            threading.Thread(
                                target=self.check_own_stamina).start()
                    elif self.state == 3:
                        _tick += 1
                        if (_tick % 2) == 0:
                            threading.Thread(
                                target=self.check_entities_on_screen).start()
                else:
                    self.log(f'[{self.name}] Game Process not found!')
                    self.log(f'[{self.name}] Waiting...')
                    time.sleep(30)
            time.sleep(0.250)
