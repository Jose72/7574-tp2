import pika
import json
from time import sleep
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.utils.counter import Counter
from src.middleware.pipe import Pipe


class LeftPipe(Pipe):

    def __init__(self, host_name, q_name, r_key, connected, processor, consumer_tag=None):
        super().__init__(host_name, q_name, r_key, connected, consumer_tag)
        self.processor = processor

    def run(self):
        self.receive_and_process(self.processor, [])
        self.close()


class TPipe:

    def __init__(self, in_pipe, out_pipes, processor):
        self.in_pipe = in_pipe
        self.out_pipes = out_pipes
        self.processor = processor

    def run(self):
        self.in_pipe.receive_and_process(self.processor, self.out_pipes)
        self.in_pipe.close()
        for op in self.out_pipes:
            op.send_end_signal()
        for op in self.out_pipes:
            op.wait_no_consumers()
            op.close()
