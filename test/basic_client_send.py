import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.client_middle import ClientMiddle


def main():
    mid = ClientMiddle('./test/client_middle_config.json')

    mid.send_tweets('./data/sample.csv')


if __name__ == "__main__":
    main()