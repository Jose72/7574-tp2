from multiprocessing import Process
import json
import sys
from time import sleep
from os import path
from src.filter.analyzer import TweetAnalyzer
from src.socket.zmq_socket import ZMQSocketPushCon, ZMQSocketPullCon


class Worker:

    def __init__(self, vent_address, vent_port, sink_address, sink_port):
        super().__init__()

        #
        self.pull_sock = ZMQSocketPullCon(vent_address, vent_port)

        #
        self.push_sock = ZMQSocketPushCon(sink_address, sink_port)

        self.end = False

    def run(self):
        # get client addres from coordinator

        analayzer = TweetAnalyzer()
        counter = 0

        while not self.end:
            tweet = self.pull_sock.recv_json()

            # TO DO: save tweet in case of failure
            sleep(0.5)
            score = analayzer.analyze(tweet['text'])
            print(score)
            counter += 1

            d1 = {'score': str(score)}
            del tweet['text']
            tweet.update(d1)

            print('worker: ' + str(tweet))
            print(str(counter))
            # send to sink
            #self.push_sock.send_json(tweet)

        print(str(counter))
        print('Finished')
