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
from src.server.aggregator import TotalAggregator, NegativeTweetValidator, PositiveTweetValidator


def main():
    print("AGGREGATOR TOTAL STARTED")

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name_in'], config_info['in_q_name'], config_info['in_r_key'])
        aggregator = TotalAggregator(config_info['date_field'], config_info['aggregate_field'],
                                     PositiveTweetValidator, NegativeTweetValidator)

        end_msg_validator = EndMessageValidator
        msg_queue = Queue()
        receiver = Receiver(in_pipe, None, aggregator, end_msg_validator)

        receiver.start()

        receiver.join()

    print("AGGREGATOR TOTAL FINISHED")


if __name__ == "__main__":
    main()
