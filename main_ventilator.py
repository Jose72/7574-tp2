import sys

from src.server.ventilator import Ventilator


def main():
    vent = Ventilator('5000', '5500')
    vent.run()


if __name__ == "__main__":
    main()