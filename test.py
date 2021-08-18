import utils.constants as consts
import utils.memory as memory

from utils.vision import Vision
from utils.controller import Controller
from utils.game import Game

if __name__ == '__main__':
    vision = Vision()
    controller = Controller()
    game = Game(consts, memory, vision, controller)
    game.run()