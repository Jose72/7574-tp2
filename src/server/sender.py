from threading import Thread
import json
import pika.exceptions
from time import sleep


class Sender(Thread):

    def __init__(self, out_pipe, msg_queue):
        super().__init__()
        self.out_pipe = out_pipe
        self.msg_queue = msg_queue
        self.end = False

    def run(self):
        try:
            while not self.end:
                msg = self.msg_queue.get()
                if msg == 'end':
                    self.end = True
                    continue
                self.out_pipe.send(msg)

            sleep(5)
            self.out_pipe.send_end_signal()
            self.out_pipe.wait_no_consumers()

        except pika.exceptions.ConnectionClosedByBroker:
            pass


