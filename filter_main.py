import json
import sys
from os import path
from multiprocessing import Queue
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.pipe import Pipe
from src.server.filter import Filter
from src.server.receiver import Receiver
from src.server.sender import Sender
from src.server.analyzer import EndMessageValidator


def main():
    print("FILTER STARTED")
    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name'], config_info['in_q_name'], config_info['in_r_key'])
        out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'])
        f_filter = Filter(config_info['fields'], config_info['conditions'], config_info['remove'])

        end_msg_validator = EndMessageValidator
        msg_queue = Queue()
        receiver = Receiver(in_pipe, [msg_queue], f_filter, end_msg_validator)
        sender = Sender(out_pipe, msg_queue, end_msg_validator)

        sender.start()
        receiver.start()

        sender.join()
        receiver.join()

    print("FILTER FINISHED")


if __name__ == "__main__":
    main()