import time
from typing import Union

import utils.constants as consts
import utils.memory as memory
import utils.logic as logic
from utils.types import Bot


class BotThread(Bot):
    def __init__(self, name: Union[str, None] = None):
        super(BotThread, self).__init__()
        if name != None:
            self.name = name

    def setState(self, state: int) -> None:
        if not self.state == 0:
            self.state = state

    def toggle_pause(self) -> None:
        if self.state == 0:
            self.state = 1
            self.log(f'[{self.name}] Un-paused')
        else:
            self.state = 0
            self.log(f'[{self.name}] Paused')
        time.sleep(0.500)

    def check_game(self) -> None:
        with memory.GameProcess() as process:
            if process == None:
                self.process_found = False
            else:
                self.process_found = True

    def call_of_the_gods_timeout(self) -> None:
        tick = 12
        self.cog_timeout = True
        while tick > 0 and self.is_paused == False:
            time.sleep(1)
            tick -= 1
        self.cog_timeout = False

    def check_own_health(self) -> None:
        healthPercentage = logic.get_missing_health_percentage(
            memory.get_health(), memory.get_health_max())
        if healthPercentage < 100:
            self.log(f'[{self.name}] Health: {healthPercentage}%')

        if healthPercentage < 98:
            newPoisonDisease = memory.get_poison_or_disease()
            if newPoisonDisease != self.last_poison_disease:
                self.last_poison_disease = newPoisonDisease
                if newPoisonDisease > 0:  # Check if we are now poisoned or diseased
                    self.log('PoisonDisease: {bot.last_poison_disease}')
                    if self.cog_timeout == False:  # Check if we aren't waiting on cog cooldown
                        self.worker_queue.add('use_call_of_the_gods_spell')
                        return

        if healthPercentage < 35:
            self.worker_queue.add('use_healing_potion')
        elif healthPercentage < 80:
            self.worker_queue.add('use_healing_spell')

    def check_own_stamina(self) -> None:
        ownStamina = memory.get_stamina()

        if ownStamina < 40:
            self.log(f'[Attacker] Stamina: {ownStamina}')
            self.worker_queue.add('use_stamina_potion')

    def check_mouse_id(self) -> None:
        id = memory.get_mouse_id()
        self.log(f'[{self.name}] get_mouse_id: {id}')
        gameWindow = logic.get_game_window_center()
        self.log(f'[{self.name}] get_game_window_center: {gameWindow}')
        selfCoords = logic.get_own_screen_coords()
        self.log(f'[{self.name}] get_own_screen_coords: {selfCoords}')

    def entity_data(self) -> None:
        entities = []
        selfLoc = memory.get_own_location()
        self.log(f'[{self.name}] Getting entities on screen...')
        for offset in consts.SCREEN_ENTITY_OFFSETS:
            for i in range(1):
                hexCode = hex(offset + (i * 4))
                entity = memory.get_entity_data(hexCode)
                if entity['id'] != 0 and entity['name'] != '' and not logic.is_known_pet(entity['name']):
                    distance = logic.get_distance_apart(
                        selfLoc, entity['coords'])
                    if distance[0] <= 14 and distance[0] >= -13 and distance[1] <= 12 and distance[1] >= -12:
                        entity['distance'] = distance
                        entity['percentage'] = logic.get_missing_health_percentage(
                            entity['hp'][0], entity['hp'][1])
                        entities.append(entity)
        entities = logic.sort_by(logic.filter(
            entities, 'id'), 'percentage')
        self.log(
            f'[{self.name}] entity_data names: {logic.flatten(entities, "name")}')
        self.log(
            f'[{self.name}] entity_data percentages: {logic.flatten(entities, "percentage")}')

    def buff_mouse_entity(self) -> None:
        self.worker_queue.add('buff_mouse_entity')

    def buff_selected_entity(self) -> None:
        self.worker_queue.add('buff_selected_entity')

    def set_protect(self) -> None:
        if memory.get_follower_id() > 0:
            memory.set_follower_state(13)

    def get_selected_entity(self) -> None:
        self.log(f'[{self.name}] SelectedEntity: {self.selected_entity}')

    def check_system_message(self) -> None:
        message = memory.get_system_message()
        if message != '' and message != 0:
            self.log(f'[{self.name}] get_system_message: {message}')

    def check_guild_message(self) -> None:
        message = memory.get_guild_message()
        if message != '' and message != 0:
            self.log(f'[{self.name}] get_guild_message: {message}')

    def check_totems_and_food(self) -> None:
        chatLogs = logic.get_last_channel_logs('Say', 2)

        if logic.logs_have_message(chatLogs, 'The effect from your food has faded', 'Eating the food'):
            self.worker_queue.add('use_food')
        if logic.logs_have_message(chatLogs, 'Your added health regen has faded', 'Your health and stamina regen increase'):
            self.worker_queue.add('use_regeneration_totem')
        if logic.logs_have_message(chatLogs, 'Your added stamina regen has faded', 'Your health and stamina regen increase'):
            self.worker_queue.add('use_regeneration_totem')
        if logic.logs_have_message(chatLogs, 'Your added strength has faded', 'You feel added strength'):
            self.worker_queue.add('use_class_totem')
        if logic.logs_have_message(chatLogs, 'Your added dexterity has faded', 'You feel added dexterity'):
            self.worker_queue.add('use_class_totem')
        if logic.logs_have_message(chatLogs, 'Your added intelligence has faded', 'You feel added intelligence'):
            self.worker_queue.add('use_class_totem')
        if logic.logs_have_message(chatLogs, 'Your added constitution has faded', 'You feel added constitution'):
            self.worker_queue.add('use_class_totem')
        if logic.logs_have_message(chatLogs, 'Your attack speed returns to normal', 'Your attack speed has been increased'):
            self.worker_queue.add('use_werewolf_totem')
