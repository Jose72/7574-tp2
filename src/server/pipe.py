import pika
import json
from time import sleep


class Pipe:

    def __init__(self, host_name, q_name, r_key, consumer_tag=None):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)
        self.consumer_tag = consumer_tag

    def send(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=json.dumps(message),
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )

    def receive_and_process(self, processor, msg_queues):

        q_name = self.q_name
        c_tag = self.consumer_tag

        def callback(ch, method, properties, body):
            b = json.loads(body)

            ch.basic_ack(delivery_tag=method.delivery_tag)

            if b == 'end':
                for mq in msg_queues:
                    mq.put(b)

                q_dec = ch.queue_declare(q_name, durable=True, passive=True)
                cc = q_dec.method.consumer_count
                #print("consumers: {}".format(cc))
                if not (cc == 1):
                    ch.basic_publish(exchange='',
                                     routing_key=self.routing_key,
                                     body=json.dumps('end'),
                                     properties=pika.BasicProperties(delivery_mode=2)
                                     )

                ch.basic_cancel(c_tag)
                return

            if processor:
                result = processor.process(b)
            else:
                result = b

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
        self.send('end')

    def get_consumer_count(self):
        q_declare_ok = self.channel.queue_declare(self.q_name, durable=True, passive=True)
        return q_declare_ok.consumer_count()

