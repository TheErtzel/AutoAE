from utils.controller import Controller
from utils.attacker import AttackerThread


def main():
    controller = Controller()
    attacker = AttackerThread(kwargs={'controller': controller})
    attacker.start()


if __name__ == '__main__':
    main()
