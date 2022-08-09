import json

from kafka.producer import KafkaProducer

from config.kafka_config import BOOTSTRAP_SERVER, TOPIC
from consts.consts import DECODE_FORMAT
from tests.data_generator import DataGenerator


class KafkaPublisher:
    def __init__(self, topic=TOPIC, bootstrap_server=BOOTSTRAP_SERVER):
        self.topic = topic
        self.bootstrap_server = bootstrap_server
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_server)

    def publish(self, payload: str):
        self.producer.send(self.topic, json.dumps(payload).encode(DECODE_FORMAT)).get()
        print("Published Message to Kafka topic{}:\n {}".format(payload, self.topic))


if __name__ == "__main__":
    generated_message = DataGenerator.generate_base_input_model()

    publisher = KafkaPublisher()
    publisher.publish(generated_message)
