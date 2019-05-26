import pika
import json
from time import sleep
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.utils.counter import Counter

class Pipe:

    def __init__(self, host_name, q_name, r_key, connected, consumer_tag=None):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)
        self.consumer_tag = consumer_tag
        self.connected = connected

    def send(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=json.dumps(message),
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )

    # receives incoming msg from rabbit queue
    # process them using a processor object
    # and puts them into the queues
    def receive_and_process(self, processor, msg_queues):

        end_counter = Counter(self.connected)
        q_name = self.q_name
        c_tag = self.consumer_tag

        def callback(ch, method, properties, body):
            b = json.loads(body)

            ch.basic_ack(delivery_tag=method.delivery_tag)

            # check for end msg, if so close
            if b == 'end':
                #print('end')
                if end_counter.increment():
                    #print('end')
                    for mq in msg_queues:
                        mq.put(b)

                    ch.basic_cancel(c_tag)

                return

            # process the msg
            if processor:
                result = processor.process(b)
            else:
                result = b

            # put processed msg into queue
            if result is not None:
                for mq in msg_queues:
                    mq.put(result)

        self.channel.basic_consume(queue=self.q_name,
                                   on_message_callback=callback,
                                   consumer_tag=self.consumer_tag)

        self.channel.start_consuming()

    def close(self):
        self.connection.close()

    def send_end_signal(self):
        cc = self.get_consumer_count()
        for i in range(0, cc):
            self.send('end')

    def wait_no_consumers(self, secs=0.5):
        cc = self.get_consumer_count()
        while not (cc == 0):
            sleep(secs)
            cc = self.get_consumer_count()
        self.channel.queue_purge(self.q_name)

    def get_consumer_count(self):
        q_declare_ok = self.channel.queue_declare(self.q_name, durable=True, passive=True)
        return q_declare_ok.method.consumer_count


class ControlPipe:
    def __init__(self, host_name, q_name, r_key, producer_count):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)
        self.producer_count = producer_count

    def producer_end(self):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=json.dumps('end'),
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )


