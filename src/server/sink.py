from multiprocessing import Process
import json
import sys
from os import path
import zmq

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.socket.zmq_socket import ZMQSocketPub, ZMQSocketPull


class Sink:

    def __init__(self, pull_port, publish_port):
        super().__init__()

        #
        self.pub_sock = ZMQSocketPub('*', publish_port)

        #
        self.pull_sock = ZMQSocketPull('*', pull_port)

        self.end = False

    def run(self):
        # get client addres from coordinator

        counter = 0

        while not self.end:
            tweet = self.pull_sock.recv_json()
            #print(tweet)

            # end signal
            if tweet == {"end": True}:
                self.end = True
                continue

            counter += 1

            print

        print('Sink - Finished')


