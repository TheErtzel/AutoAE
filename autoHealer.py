from utils.controller import Controller
from utils.healer import HealerThread


def main():
    controller = Controller()
    healer = HealerThread(kwargs={'controller': controller})
    healer.start()


if __name__ == '__main__':
    main()
