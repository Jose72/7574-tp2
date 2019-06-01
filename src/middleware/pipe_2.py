import pika
import json
from time import sleep
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.utils.counter import Counter
from src.middleware.pipe import Pipe
from src.processing.factory import ProcessorFactory


class LeftPipe(Pipe):

    def __init__(self, host_name, q_name, r_key, connected, processor, consumer_tag=None):
        super().__init__(host_name, q_name, r_key, connected, consumer_tag)
        self.processor = processor

    def run(self):
        self.receive_and_process(self.processor)
        self.close()


class TPipe:

    def __init__(self, in_config, out_configs, processor_config, consumer_tag):

        self.in_pipe = Pipe(in_config['host_name_in'], in_config['in_q_name'],
                            in_config['in_r_key'], in_config["producers"], consumer_tag)

        self.out_pipes = []
        for oc in out_configs:
            self.out_pipes.append(
                Pipe(oc['host_name_out'], oc['out_q_name'], oc['out_r_key'], oc["consumers"])
            )

        self.processor = ProcessorFactory.create(processor_config, self.out_pipes)

    def run(self):
        self.in_pipe.receive_and_process(self.processor)
        self.in_pipe.close()
        self.processor.close()
        for op in self.out_pipes:
            op.send_end_signal()
        for op in self.out_pipes:
            op.wait_no_consumers()
            op.close()


