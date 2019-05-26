import json
from time import sleep
import sys
import uuid
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.pipe import Pipe
from src.server.receiver import Receiver
from src.processing.aggregator import TotalAggregator, NegativeTweetValidator, PositiveTweetValidator


def main():
    print("AGGREGATOR TOTAL STARTED")

    consumer_tag = uuid.uuid1().hex

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name_in'], config_info['in_q_name'], config_info['in_r_key'],
                       sys.argv[2], consumer_tag)
        aggregator = TotalAggregator(config_info['date_field'], config_info['aggregate_field'],
                                     PositiveTweetValidator, NegativeTweetValidator)

        receiver = Receiver(in_pipe, [], aggregator)

        receiver.start()

        receiver.join()

        aggregator.print()

        aggregator.save_to_file()

        in_pipe.close()

    print("AGGREGATOR TOTAL FINISHED")


if __name__ == "__main__":
    main()
