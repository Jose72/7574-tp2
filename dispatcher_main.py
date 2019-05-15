import sys
import json

from src.server.dispatcher import Dispatcher
from src.server.pipe import Pipe


def main():
    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()
        out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'])
        Dispatcher.dispatch('./data/sample.csv', config_info['fieldnames'], out_pipe)


if __name__ == "__main__":
    main()
