import utils.constants as consts
import utils.memory as memory
import utils.ocr as ocr

from utils.vision import Vision
from utils.controller import Controller
from utils.bot import BotThread

if __name__ == '__main__':
    vision = Vision()
    controller = Controller()
    bot = BotThread(kwargs={'consts': consts, 'memory': memory,
                            'ocr': ocr, 'vision': vision, 'controller': controller})
    bot.start()
