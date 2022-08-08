from config.kafka_config import TOPIC, BOOTSTRAP_SERVER
from consts.consts import DECODE_FORMAT
from pipeline import Pipeline
from read.reader import Reader

from kafka.consumer import KafkaConsumer


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


if __name__ == "__main__":
    kafka_reader = KafkaReader()
    kafka_reader.listen(callback=Pipeline.callback)
