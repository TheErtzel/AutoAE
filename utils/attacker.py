import time
import keyboard
import threading
import numpy as np

from utils.bot import BotThread
from utils.queue import LoggerThread, ConsumerThread


class AttackerThread(BotThread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super().__init__(name)
        self.state = 0
        self.logger_queue = LoggerThread()
        self.logger_queue.setDaemon(True)
        self.logger_queue.start()
        self.worker_queue = ConsumerThread(kwargs={'bot': self})
        self.worker_queue.setDaemon(True)
        self.worker_queue.start()
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
        keyboard.add_hotkey('ctrl+end', self.set_protect)
        keyboard.add_hotkey('ctrl+alt', self.get_selected_entity)

    def check_target(self) -> None:
        if not self.looking_for_target:
            self.worker_queue.add('target_new_enemy')

    def run(self) -> None:
        self.log(
            f'[{self.name}] Started! press [pause] to toggle pause/un-pause')
        _tick = 0

        while True:
            # threading.Thread(target=self.check_system_message).start()
            if self.state == 1:
                self.check_game()
                if self.process_found:
                    _tick += 1
                    threading.Thread(target=self.check_system_message).start()
                    threading.Thread(target=self.check_guild_message).start()
                    threading.Thread(
                        target=self.check_totems_and_food).start()
                    threading.Thread(target=self.check_target).start()

                    if (_tick % 10) == 0:
                        threading.Thread(target=self.check_own_health).start()
                        threading.Thread(target=self.check_own_stamina).start()
                else:
                    self.log(f'[{self.name}] Game Process not found!')
                    self.log(f'[{self.name}] Waiting...')
                    time.sleep(30)
            time.sleep(0.250)
