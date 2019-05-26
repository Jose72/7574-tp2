import json
import uuid
import sys
from multiprocessing import Queue
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.pipe import Pipe
from src.processing.analyzer import TextProcessor
from src.server.receiver import Receiver
from src.server.sender import Sender


def main():
    print("TEXT PROCESSING STARTED")

    consumer_tag = uuid.uuid1().hex

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        in_pipe = Pipe(config_info['host_name_in'], config_info['in_q_name'], config_info['in_r_key'],
                       sys.argv[2], consumer_tag)
        out_pipe_a1 = Pipe(config_info['host_name_out'], config_info['out_q_name_a1'],
                           config_info['out_r_key_a1'], sys.argv[3])
        out_pipe_a2 = Pipe(config_info['host_name_out'], config_info['out_q_name_a2'],
                           config_info['out_r_key_a2'], sys.argv[4])
        t_processor = TextProcessor(config_info['field'], config_info['new_field'], config_info['remove'])

        msg_queue_1 = Queue()
        msg_queue_2 = Queue()
        msg_queues = [msg_queue_1, msg_queue_2]
        receiver = Receiver(in_pipe, msg_queues, t_processor)
        sender_1 = Sender(out_pipe_a1, msg_queue_1)
        sender_2 = Sender(out_pipe_a2, msg_queue_2)

        sender_1.start()
        sender_2.start()
        receiver.start()

        sender_1.join()
        sender_2.join()
        receiver.join()

    print("TEXT PROCESSING FINISHED")


if __name__ == "__main__":
    main()