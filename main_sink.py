import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.sink import Sink


def main():
    w = Sink('6000', '6060')
    w.run()


if __name__ == "__main__":
    main()