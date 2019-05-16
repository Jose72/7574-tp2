import pika
import json
from time import sleep


class Pipe:

    def __init__(self, host_name, q_name, r_key):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)

    def send(self, message):
        self.channel.basic_publish(exchange="",
                                   routing_key=self.routing_key,
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )

    def receive_and_process(self, processor, out_pipe):

        def callback(ch, method, properties, body):
            b = json.loads(body)
            result = processor.process(b)
            #print(json.dumps(result))
            #sleep(0.1)
            if out_pipe:
                out_pipe.send(json.dumps(result))

            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=self.q_name,
                                   on_message_callback=callback)

        self.channel.start_consuming()

    def close(self):
        self.connection.close()


class SubPipe:
    def __init__(self, host_name, q_name, r_key):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)