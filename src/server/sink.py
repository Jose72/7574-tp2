import sys
from os import path
import zmq

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.data.records import TotalTweetRecord, UsersTweetRecords
from src.socket.zmq_socket import ZMQSocketPub, ZMQSocketPullBind


class Sink:

    def __init__(self, pull_port, publish_port):
        super().__init__()

        self.pub_sock = ZMQSocketPub('*', publish_port)

        self.pull_sock = ZMQSocketPullBind('*', pull_port)

        self.total_tweet_rec = TotalTweetRecord()

        self.user_tweet_rec = UsersTweetRecords(3)

        self.end = False

    def run(self):
        # get client addres from coordinator
        print('Sink - Started')

        counter = 0

        while not self.end:
            tweet = self.pull_sock.recv_json()

            print(tweet)

            t_score = int(tweet['score'])
            t_uid = tweet['author_id']
            t_date = tweet['created_at']

            warning = False
            if t_score > 0:
                self.total_tweet_rec.increment_positive_tweet()
            else:
                self.total_tweet_rec.increment_negative_tweet()
                warning = self.user_tweet_rec.increment_negative_tweet(t_uid, t_date)

            if warning:
                print("Warning - user: {} has reached 3 knows too much. Terminate him".format(t_uid))

            counter += 1

            # hardcoded for test since there is no termination signal yet
            if counter == 94:
                self.end = True

        print(counter)

        self.total_tweet_rec.print()
        self.user_tweet_rec.print()

        print('Sink - Finished')


