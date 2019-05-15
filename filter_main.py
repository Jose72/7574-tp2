import json
import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.pipe import Pipe
from src.server.filter import Filter


def main():
    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name'], config_info['in_q_name'], config_info['in_r_key'])
        out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'])
        f_filter = Filter(config_info['fields'], config_info['conditions'], config_info['remove'])

        while True:
            msg = in_pipe.receive_and_process(f_filter, out_pipe)

            #print(msg)


if __name__ == "__main__":
    main()