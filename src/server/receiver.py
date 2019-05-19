from threading import Thread

import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.server.pipe import PipeError


class Receiver(Thread):

    def __init__(self, in_pipe, msg_queue, msg_processor, end_msg_validator):
        super().__init__()
        self.in_pipe = in_pipe
        self.msg_queue = msg_queue
        self.msg_processor = msg_processor
        self.end_msg_validator = end_msg_validator
        self.end = False

    def run(self):
        try:
            self.in_pipe.receive_and_process(self.msg_processor, self.msg_queue, self.end_msg_validator)
        except PipeError:
            pass
        finally:
            self.in_pipe.close()
