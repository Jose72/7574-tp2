import json
from time import sleep
import uuid
import sys
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.pipe import Pipe
from src.server.receiver import Receiver
from src.processing.sink import UserSink


def main():
    print("SINK USERS STARTED")

    consumer_tag = uuid.uuid1().hex

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name_in'], config_info['in_q_name'], config_info['in_r_key'],
                       sys.argv[2], consumer_tag)
        sink = UserSink(config_info['user_field'], config_info['aggregate_field'])

        receiver = Receiver(in_pipe, [], sink)

        receiver.start()

        receiver.join()

        sink.print()

        sink.save_to_file()


    print("SINK USERS FINISHED")


if __name__ == "__main__":
    main()
