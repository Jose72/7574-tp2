from multiprocessing import Process
import json
import sys
from os import path
import zmq

from src.socket.zmq_socket import ZMQSocketPushBind, ZMQSocketRep


class Ventilator:

    def __init__(self, config_file):
        super().__init__()
        with open(config_file, 'r+') as c_file:
            config_info_post = json.load(c_file)
            c_file.close()

        #
        self.req_sock = ZMQSocketRep('*', config_info_post['listen_port'])

        #
        self.push_sock = ZMQSocketPushBind('127.0.0.1', config_info_post['push_port'])

        self.end = False

    def run(self):
        # get client addres from coordinator

        counter = 0
        counter_inbound = 0

        while not self.end:
            tweet = self.req_sock.recv_json()
            #print(tweet)
            # TO DO: save tweet in case of failure
            r = self.req_sock.send_string('OK')

            # end signal
            if tweet == {"end": True}:
                self.end = True
                continue

            counter += 1

            # if its not a user tweeter then continue
            if not tweet['inbound']:
                continue

            counter_inbound += 1

            # dont care about those fields
            del tweet['inbound']
            del tweet['response_tweet_id']
            del tweet['in_response_to_tweet_id']

            print(tweet)

            # filter
            # send to worker
            self.push_sock.send_json(tweet)

        print(str(counter_inbound))
        print('Finished')


