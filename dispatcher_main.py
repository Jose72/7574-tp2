import sys
import json

from src.server.dispatcher import Dispatcher
from src.middleware.pipe import Pipe


def main():
    print("DISPATCHER STARTED")
    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()
        out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'], sys.argv[2])
        Dispatcher.dispatch('./data/sample.csv', config_info['fieldnames'], out_pipe)

        out_pipe.send_end_signal()
        out_pipe.wait_no_consumers()
        out_pipe.close()

    print("DISPATCHER FINISHED")


if __name__ == "__main__":
    main()
