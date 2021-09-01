import utils.constants as consts
import utils.memory as memory
import utils.ocr as ocr

from utils.vision import Vision
from utils.controller import Controller
from utils.attacker import AttackerThread

if __name__ == '__main__':
    vision = Vision()
    controller = Controller()
    attacker = AttackerThread(kwargs={'consts': consts, 'memory': memory,
                                      'ocr': ocr, 'vision': vision, 'controller': controller})
    attacker.start()
