from threading import Thread
import queue
import json
import pika.exceptions
from time import sleep


class Flusher(Thread):

    def __init__(self, out_pipe, msg_queue, flushable, timeout):
        super().__init__()
        self.out_pipe = out_pipe
        self.flushable = flushable
        self.msg_queue = msg_queue
        self.timeout = timeout
        self.end = False

    def run(self):
        try:
            while not self.end:
                # wait 'timeout' for the end message
                try:
                    msg = self.msg_queue.get(timeout=self.timeout)
                    if msg == 'end':
                        self.end = True
                        continue
                except queue.Empty:
                    pass

                #flush the data to the pipe
                self.flushable.flush(self.out_pipe)

            # flush whatever is left
            self.flushable.flush(self.out_pipe)

            self.out_pipe.send_end_signal()
            self.out_pipe.wait_no_consumers()

        except pika.exceptions.ConnectionClosedByBroker:
            pass
