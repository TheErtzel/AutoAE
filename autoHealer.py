from utils.vision import Vision
from utils.controller import Controller
from utils.healer import HealerThread


def main():
    vision = Vision()
    controller = Controller()
    healer = HealerThread(kwargs={'vision': vision, 'controller': controller})
    healer.start()


if __name__ == '__main__':
    main()
