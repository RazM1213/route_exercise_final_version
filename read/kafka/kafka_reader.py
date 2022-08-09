from kafka.consumer import KafkaConsumer

from config.kafka_config import TOPIC, BOOTSTRAP_SERVER
from read.reader import Reader


class KafkaReader(Reader):
    def __init__(self, topic=TOPIC, bootstrap_server=BOOTSTRAP_SERVER):
        self.topic = topic
        self.bootstrap_server = bootstrap_server
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.bootstrap_server)
        print("Kafka server started...")
        print(f"[X] Waiting for data on topic: {self.topic}...")

    def listen(self, callback):
        for message in self.consumer:
            callback(message)
