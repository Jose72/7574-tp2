import csv
import json
import zmq
from src.socket.zmq_socket import ZMQSocketReq, ZMQSocketRep


class ClientMiddle():

    def __init__(self, config_file):
        with open(config_file, 'r+') as c_file:
            config_info_post = json.load(c_file)
        self.serv_address = config_info_post['serv_address']
        self.serv_port = config_info_post['serv_port']
        self.my_port = config_info_post['my_port']
        self.serv_sock = ZMQSocketReq(self.serv_address, self.serv_port)
        self.can_send = True

    def send_tweets(self, file):

        if self.can_send:
            fieldnames = ['tweet_id', 'author_id', 'inbound', 'created_at',
                          'text', 'response_tweet_id', 'in_response_to_tweet_id']
            with open(file, 'r') as t_file:

                reader = csv.DictReader(t_file, delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
                for e in reader:
                    print('1c---')
                    r = self.serv_sock.send_json(e)
                    print('2c---' + str(r))
                    r = self.serv_sock.recv_string()
                    print('3c---' + str(r))

                t_file.close()

            self.serv_sock.send_json({"end": True})
            self.serv_sock.recv_string()
            # wait for response of server

