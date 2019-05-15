import pika
import json


class Pipe:

    def __init__(self, host_name, q_name, r_key):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name))
        self.channel = self.connection.channel()
        self.q_name = q_name
        self.channel.queue_declare(queue=q_name, durable=True)
        self.routing_key = r_key

    def send(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2)
                                   )

    def receive_and_process(self, processor, out_pipe):

        def callback(ch, method, properties, body):
            b = json.loads(body)
            result = processor.process(b)
            print(json.dumps(result))
            if out_pipe:
                out_pipe.send(json.dumps(result))

        self.channel.basic_consume(queue=self.q_name,
                                   on_message_callback=callback,
                                   auto_ack=True)

        self.channel.start_consuming()
