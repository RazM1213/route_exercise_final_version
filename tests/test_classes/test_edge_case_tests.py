from config import path_config
from consts.json_fields import EXTRA_FIELD, BIRTHDATE, AGE, STUDENT_DETAILS, FIRST_NAME, LAST_NAME, BEHAVIOUR_GRADE, IS_GOOD_BEHAVIOUR
from tests.send_generated_input_script.data_generator import DataGenerator
from tests.test_base import TestBase


class EdgeCaseTests(TestBase):
    def test_send_same_body_twice(self):
        generated_input = DataGenerator.generate_base_input_model()

        self.send_body(generated_input)
        self.send_body(generated_input)

        self.assertTrue(1, len(self.get_docs(expected_docs=1)))

    def test_two_text_files_saved_success(self):
        self._PUBLISHER.generate_data(documents_to_publish=2)

        self.assertEqual(2, len(self.get_docs(expected_docs=2)))

    def test_existing_student_file_overrides(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][FIRST_NAME] = "test"
        generated_input[STUDENT_DETAILS][LAST_NAME] = "tester"
        generated_input[BEHAVIOUR_GRADE] = 6

        self.send_body(generated_input)
        generated_input[BEHAVIOUR_GRADE] = 3
        self.send_body(generated_input)
        file_name = self.get_docs(expected_docs=1)[0]

        self.assertEqual(1, len(self.get_docs(expected_docs=1)))
        actual_output = self.read_from_file(f"{path_config.TEST_STUDENTS_DIR_PATH}/{file_name}")
        self.assertEqual(actual_output[IS_GOOD_BEHAVIOUR], False)

    def test_send_non_json_body_failure(self):
        input_body = """a"""

        self.send_body(input_body)

        self.assertEqual(0, len(self.get_docs(expected_docs=0)))

    def test_extra_field_body_text_file_saved_success(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[EXTRA_FIELD] = "test"

        self.send_body(input_model)

        self.assertEqual(1, len(self.get_docs(expected_docs=1)))

    def test_birthdate_not_compatible_with_age(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[BIRTHDATE] = "27/06/2000"
        input_model[AGE] = 30

        self.send_body(input_model)

        self.assertEqual(0, len(self.get_docs(expected_docs=0)))

    def test_valid_body_after_invalid_body(self):
        invalid_generated_input = DataGenerator.generate_base_input_model()
        valid_generated_input = DataGenerator.generate_base_input_model()
        invalid_generated_input[STUDENT_DETAILS][FIRST_NAME] = None

        self.send_body(invalid_generated_input)
        self.send_body(valid_generated_input)
        actual_output = self.read_from_file(f"{path_config.TEST_STUDENTS_DIR_PATH}/{self.get_docs(expected_docs=1)[0]}")

        self.assertEqual(1, len(self.get_docs(expected_docs=1)))
        self.assertEqual(valid_generated_input[STUDENT_DETAILS][FIRST_NAME], actual_output[STUDENT_DETAILS][FIRST_NAME])
