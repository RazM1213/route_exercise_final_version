import pika

from config import rabbit_mq_config
from config.rabbit_mq_config import QUEUE
from read.reader import Reader


class RabbitMqReader(Reader):
    def __init__(self, queue=QUEUE):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self.queue = queue
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue)

    def listen(self, callback):
        print("RabbitMq server started...")
        print(f"[X] Waiting for data on queue: {self.queue}...")
        self._channel.basic_consume(
            queue=self.queue,
            on_message_callback=lambda ch, method, properties, body: callback(body),
            auto_ack=True
        )
        self._channel.start_consuming()
