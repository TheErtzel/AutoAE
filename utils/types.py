import threading
from typing import Any, Union, Dict, List

from utils.queue import LoggerThread, ConsumerThread


class Bot(threading.Thread):
    name: str = 'Bot'
    state: int = 0
    logger_queue: LoggerThread = None
    worker_queue: ConsumerThread = None
    background_queue: ConsumerThread = None
    process_found: bool = False
    usedSpell: bool = False
    cog_timeout: bool = False
    last_poison_disease: int = 0
    looking_for_target: bool = False
    entities_on_screen: List[Dict[str, Any]] = []
    npcs_on_screen: List[Dict[str, Any]] = []
    non_player_ids: List[int] = []
    selected_entity: Union[Dict[str, Any], None] = None
    ignored_ids: List[int] = []
    fizzle_count: int = 0

    def __init__(self, name: Union[str, None] = None):
        super(Bot, self).__init__()
        if name != None:
            self.name = name

    def log(self, text: str) -> None:
        self.logger_queue.add(text)
