import pika
import json
from time import sleep
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.pipe import Pipe
from src.processing.factory import ProcessorFactory


class TPipe:

    def __init__(self, in_config, out_configs, processor, consumer_tag):

        # create the in pipe
        self.in_pipe = Pipe(in_config['host_name_in'], in_config['in_q_name'],
                            in_config['in_r_key'], in_config["producers"], consumer_tag)

        # create the out pipes
        self.out_pipes = []
        for oc in out_configs:
            self.out_pipes.append(
                Pipe(oc['host_name_out'], oc['out_q_name'], oc['out_r_key'], oc["consumers"])
            )

        # processor
        self.processor = processor

    def send(self, data):
        for d in data:
            for op in self.out_pipes:
                op.send(d)

    def run(self):

        # receive and process, close the in pipe when done
        self.in_pipe.receive_and_process(self.processor, self.out_pipes)
        self.in_pipe.close()

        # send data left
        r_data = self.processor.flush()
        self.send(r_data)

        # finish if processor has something else to do
        self.processor.close()

        # send end signals, wait and close the out pipes
        for op in self.out_pipes:
            op.send_end_signal()
        for op in self.out_pipes:
            op.wait_no_consumers()
            op.close()


