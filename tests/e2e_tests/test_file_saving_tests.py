import time

from more_itertools import one

from config.elastic_config import DOCUMENT_ID
from consts.json_fields import STUDENT_DETAILS, ID
from tests.data_generator import DataGenerator
from tests.test_base import TestBase


class FileSavingTests(TestBase):
    def test_valid_document_id(self):
        generated_input = DataGenerator.generate_base_input_model()

        self.send_body(generated_input)
        time.sleep(2)

        document_id = int(one(self.get_documents_from_index(self.get_document_index(generated_input)))[DOCUMENT_ID])

        self.assertEqual(generated_input[STUDENT_DETAILS][ID], document_id)
