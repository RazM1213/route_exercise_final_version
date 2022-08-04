import datetime
import json
import os
from typing import List
from unittest import TestCase

from config import path_config
from tests.data_generator import DataGenerator
from tests.rabbit_mq_publisher import RabbitMqPublisher


class TestBase(TestCase):
    _PUBLISHER = RabbitMqPublisher()

    def setUp(self):
        self.get_docs(expected_docs=0)
        os.chdir(path_config.TEST_STUDENTS_DIR_PATH)
        if os.path.exists(path_config.TEST_STUDENTS_DIR_PATH):
            for file in os.listdir(path_config.TEST_STUDENTS_DIR_PATH):
                os.remove(os.path.join(path_config.TEST_STUDENTS_DIR_PATH, file))

    def read_from_file(self, filename: str) -> json:
        self.get_docs(expected_docs=1)

        with open(f"{path_config.TEST_STUDENTS_DIR_PATH}/{filename}", "r") as text_file:
            json_data = json.loads(text_file.read())

        return json_data

    def generate_data(self, documents_to_publish: int):
        for document in range(documents_to_publish):
            input_student = DataGenerator.generate_base_input_model()
            self.send_body(input_student)

    def send_body(self, body: dict) -> None:
        self._PUBLISHER.publish(json.dumps(body))

    @staticmethod
    def get_docs(expected_docs: int, timeout_sec: int = 3000) -> List:
        date = datetime.datetime.now() + datetime.timedelta(milliseconds=timeout_sec)
        if not expected_docs:
            while date > datetime.datetime.now():
                if len(os.listdir(path_config.TEST_STUDENTS_DIR_PATH)):
                    return os.listdir(path_config.TEST_STUDENTS_DIR_PATH)
            return os.listdir(path_config.TEST_STUDENTS_DIR_PATH)
        else:
            while len(os.listdir()) != expected_docs and date > datetime.datetime.now():
                result = os.listdir(path_config.TEST_STUDENTS_DIR_PATH)
                if len(result) == expected_docs:
                    return result
            return os.listdir(path_config.TEST_STUDENTS_DIR_PATH)
