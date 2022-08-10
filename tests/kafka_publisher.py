import json

from kafka.producer import KafkaProducer

from config.kafka_config import BOOTSTRAP_SERVER, TOPIC
from consts.consts import DECODE_FORMAT
from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, SUBJECT_GRADES, SUBJECT, GRADES
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
    generated_message[STUDENT_DETAILS][FIRST_NAME] = "Bill"
    generated_message[STUDENT_DETAILS][LAST_NAME] = "Gates"
    generated_message[SUBJECT_GRADES][0][SUBJECT] = "Computer Science"
    generated_message[SUBJECT_GRADES][0][GRADES] = [100, 100, 100]

    publisher = KafkaPublisher()
    publisher.publish(generated_message)
