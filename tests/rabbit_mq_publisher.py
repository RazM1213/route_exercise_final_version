import pika

from config import rabbit_mq_config


class RabbitMqPublisher:
    def __init__(self, queue: str, routing_key: str):
        self.routing_key = routing_key
        self.queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self.channel = self._connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, payload: str):
        self.channel.basic_publish(
            exchange=rabbit_mq_config.EXCHANGE,
            routing_key=self.routing_key,
            body=payload
        )

        print("Published Message:\n {}".format(payload))
