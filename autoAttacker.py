from utils.attacker import AttackerThread


def main():
    attacker = AttackerThread(name='Attacker')
    attacker.start()


if __name__ == '__main__':
    main()
