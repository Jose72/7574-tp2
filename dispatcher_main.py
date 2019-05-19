import sys
import json

from src.server.dispatcher import Dispatcher
from src.server.pipe import Pipe
from src.server.analyzer import EndMessageValidator


def main():
    print("DISPATCHER STARTED")
    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()
        out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'])
        Dispatcher.dispatch('./data/sample.csv', config_info['fieldnames'], out_pipe)
        #SEND END SIGNAL
        #out_pipe.send(json.dumps(EndMessageValidator.create_end_msg()))
    print("DISPATCHER FINISHED")


if __name__ == "__main__":
    main()
