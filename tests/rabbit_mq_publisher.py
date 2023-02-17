import pika

from config import rabbit_mq_config
from config.rabbit_mq_config import ROUTING_KEY, QUEUE


class RabbitMqPublisher:
    def __init__(self, queue=QUEUE, routing_key=ROUTING_KEY):
        self.routing_key = routing_key
        self.queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self.channel = self._connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, payload):
        self.channel.basic_publish(
            exchange=rabbit_mq_config.EXCHANGE,
            routing_key=self.routing_key,
            body=payload
        )

        print("Published Message:\n {}".format(payload))
