from utils.vision import Vision
from utils.controller import Controller
from utils.attacker import AttackerThread


def main():
    vision = Vision()
    controller = Controller()
    attacker = AttackerThread(
        kwargs={'vision': vision, 'controller': controller})
    attacker.start()


if __name__ == '__main__':
    main()
