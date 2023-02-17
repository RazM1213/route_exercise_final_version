import time

from parameterized import parameterized

from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, ID, SUBJECT_GRADES, SUBJECT, GRADES, BIRTHDATE, AGE, GENDER, BEHAVIOUR_GRADE
from tests.data_generator import DataGenerator
from tests.test_base import TestBase


class MissingFieldTests(TestBase):
    @parameterized.expand([
        [STUDENT_DETAILS],
        [SUBJECT_GRADES],
        [BIRTHDATE],
        [AGE],
        [GENDER],
        [BEHAVIOUR_GRADE]
    ])
    def test_missing_fields_body_failure(self, field):
        input_model = DataGenerator.generate_base_input_model()
        input_model[field] = None

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    @parameterized.expand([
        [FIRST_NAME],
        [LAST_NAME],
        [ID]
    ])
    def test_missing_fields_student_details_failure(self, field):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][field] = None

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    @parameterized.expand([
        [SUBJECT],
        [GRADES]
    ])
    def test_missing_fields_student_details_failure(self, field):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[SUBJECT_GRADES][0][field] = None

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())
