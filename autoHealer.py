from utils.healer import HealerThread


def main():
    healer = HealerThread(name='Healer')
    healer.start()


if __name__ == '__main__':
    main()
