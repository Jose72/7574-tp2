import json
from multiprocessing import Queue
from time import sleep
import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.pipe import Pipe
from src.server.receiver import Receiver
from src.server.sender import Sender
from src.server.analyzer import EndMessageValidator
from src.server.aggregator import UserAggregator, NegativeTweetValidator


def main():
    print("AGGREGATOR USERS STARTED")

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name_in'], config_info['in_q_name'], config_info['in_r_key'])
        out_pipe = Pipe(config_info['host_name_out'], config_info['out_q_name'], config_info['out_r_key'])
        aggregator = UserAggregator(config_info['user_field'], config_info['aggregate_field'], NegativeTweetValidator)

        end_msg_validator = EndMessageValidator
        msg_queue = Queue()
        receiver = Receiver(in_pipe, None, aggregator, end_msg_validator)

        receiver.start()

        receiver.join()

        out_pipe.close()

    print("AGGREGATOR USERS FINISHED")


if __name__ == "__main__":
    main()