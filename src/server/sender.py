from threading import Thread
import json


class Sender(Thread):

    def __init__(self, out_pipe, msg_queue, end_msg_validator):
        super().__init__()
        self.out_pipe = out_pipe
        self.msg_queue = msg_queue
        self.end_msg_validator = end_msg_validator
        self.end = False

    def run(self):
        while not self.end:
            msg = self.msg_queue.get()
            if self.end_msg_validator.validate(msg):
                self.end = True
                continue
            self.out_pipe.send(msg)

        self.out_pipe.close()