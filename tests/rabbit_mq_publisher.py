import pika

from config import rabbit_mq_config


class RabbitMqPublisher:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self.channel = self._connection.channel()
        self.channel.queue_declare(queue=rabbit_mq_config.QUEUE)

    def publish(self, payload: str):
        self.channel.basic_publish(
            exchange=rabbit_mq_config.EXCHANGE,
            routing_key=rabbit_mq_config.ROUTING_KEY,
            body=payload
        )

        print("Published Message:\n {}".format(payload))