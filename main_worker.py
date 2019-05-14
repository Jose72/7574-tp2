import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.worker import Worker


def main():
    w = Worker('127.0.0.1', '5500', '127.0.0.1', '6000')
    w.run()


if __name__ == "__main__":
    main()