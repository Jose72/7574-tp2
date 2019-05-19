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
        self.routing_key = r_key
        self.channel.basic_qos(prefetch_count=1)

    def send(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=json.dumps(message),
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )

    def receive_and_process(self, processor, msg_queues, end_msg_valid):

        def callback(ch, method, properties, body):
            b = json.loads(body)

            if end_msg_valid.validate(b):
                for mq in msg_queues:
                    mq.put('end')

                ch.basic_ack(delivery_tag=method.delivery_tag)
                print("end messasge")
                return

            result = processor.process(b)
            #print(json.dumps(result))
            #sleep(0.1)
            if result is not None:
                for mq in msg_queues:
                    mq.put(result)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=self.q_name,
                                   on_message_callback=callback)

        self.channel.start_consuming()

    def close(self):
        self.connection.close()


class PipeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)