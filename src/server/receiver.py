from threading import Thread
import pika.exceptions
import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Receiver(Thread):

    def __init__(self, in_pipe, msg_queue, msg_processor):
        super().__init__()
        self.in_pipe = in_pipe
        self.msg_queue = msg_queue
        self.msg_processor = msg_processor
        self.end = False

    def run(self):
        try:
            self.in_pipe.receive_and_process(self.msg_processor, self.msg_queue)
        except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.StreamLostError) as e:
            pass

