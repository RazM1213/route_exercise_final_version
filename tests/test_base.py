import datetime
import json
from typing import List
from unittest import TestCase

from elasticsearch import Elasticsearch

from config import elastic_config
from config.elastic_config import HITS, SOURCE_DOCUMENT
from consts.formats import DATETIME_FORMAT
from consts.json_fields import BIRTHDATE, STUDENT_DETAILS, ID
from tests.data_generator import DataGenerator
from tests.rabbit_mq_publisher import RabbitMqPublisher


class TestBase(TestCase):
    _PUBLISHER = RabbitMqPublisher()
    _ES = Elasticsearch(
        elastic_config.LOCAL_HOST,
        basic_auth=(elastic_config.USERNAME, elastic_config.PASSWORD),
    )

    def setUp(self):
        for index in self._ES.indices.get(index="test-*"):
            self._ES.indices.delete(index=index)

    def read_from_elastic_document(self, input_dict: dict) -> json:
        return self._ES.get(index=self.get_document_index(input_dict), id=self.get_document_id(input_dict))[SOURCE_DOCUMENT]

    @staticmethod
    def generate_data(documents_to_publish: int):
        for document in range(documents_to_publish):
            input_student = DataGenerator.generate_base_input_model()
            TestBase.send_body(input_student)

    @staticmethod
    def send_body(body: dict):
        TestBase._PUBLISHER.publish(json.dumps(body))

    @staticmethod
    def get_documents_from_index(index: str) -> List:
        return TestBase._ES.search(index=index)[HITS][HITS]

    @staticmethod
    def get_document_index(input_dict: dict) -> str:
        return f"test-{datetime.datetime.strptime(input_dict[BIRTHDATE], DATETIME_FORMAT).year}"

    @staticmethod
    def get_document_id(input_dict: dict) -> int:
        return input_dict[STUDENT_DETAILS][ID]

    @staticmethod
    def get_number_of_all_documents() -> int:
        sum = 0
        for index in TestBase._ES.indices.get(index="test-*"):
            sum += len(TestBase._ES.search(index=index)[HITS][HITS])
        return sum
