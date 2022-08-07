import time

from consts.json_fields import EXTRA_FIELD, BIRTHDATE, AGE, STUDENT_DETAILS, FIRST_NAME, LAST_NAME, BEHAVIOUR_GRADE, IS_GOOD_BEHAVIOUR, SUBJECT_GRADES, GRADES, AVERAGE
from tests.data_generator import DataGenerator
from tests.test_base import TestBase


class EdgeCaseTests(TestBase):
    def test_send_same_body_twice(self):
        generated_input = DataGenerator.generate_base_input_model()

        self.send_body(generated_input)
        self.send_body(generated_input)
        time.sleep(1)

        self.assertTrue(1, self.get_number_of_all_documents())

    def test_two_text_files_saved_success(self):
        self.generate_data(documents_to_publish=2)

        time.sleep(2)

        self.assertEqual(2, self.get_number_of_all_documents())

    def test_existing_student_file_overrides(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][FIRST_NAME] = "test"
        generated_input[STUDENT_DETAILS][LAST_NAME] = "tester"
        generated_input[BEHAVIOUR_GRADE] = 6

        self.send_body(generated_input)
        generated_input[BEHAVIOUR_GRADE] = 3
        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(1, self.get_number_of_all_documents())
        actual_output = self.read_from_elastic_document(generated_input)
        self.assertFalse(actual_output[IS_GOOD_BEHAVIOUR])

    def test_send_non_json_body_failure(self):
        input_body = """a"""

        self.send_body(input_body)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_extra_field_body_text_file_saved_success(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[EXTRA_FIELD] = "test"

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(1, self.get_number_of_all_documents())

    def test_birthdate_not_compatible_with_age(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[BIRTHDATE] = "27/06/2000"
        generated_input[AGE] = 30

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_valid_body_after_invalid_body(self):
        invalid_generated_input = DataGenerator.generate_base_input_model()
        invalid_generated_input[STUDENT_DETAILS][FIRST_NAME] = None
        valid_generated_input = DataGenerator.generate_base_input_model()

        self.send_body(invalid_generated_input)
        self.send_body(valid_generated_input)
        time.sleep(2)

        actual_output = self.read_from_elastic_document(valid_generated_input)

        self.assertEqual(1, self.get_number_of_all_documents())
        self.assertEqual(valid_generated_input[STUDENT_DETAILS][FIRST_NAME], actual_output[STUDENT_DETAILS][FIRST_NAME])

    def test_valid_body_without_subjects(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[SUBJECT_GRADES] = []

        self.send_body(generated_input)
        time.sleep(2)
        actual_output = self.read_from_elastic_document(generated_input)

        self.assertEqual(1, self.get_number_of_all_documents())
        self.assertEqual(generated_input[SUBJECT_GRADES], actual_output[SUBJECT_GRADES])

    def test_valid_body_without_subject_grades(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[SUBJECT_GRADES][0][GRADES] = []

        self.send_body(generated_input)
        time.sleep(2)
        actual_output = self.read_from_elastic_document(generated_input)

        self.assertEqual(1, self.get_number_of_all_documents())
        self.assertEqual(0, actual_output[SUBJECT_GRADES][0][AVERAGE])
