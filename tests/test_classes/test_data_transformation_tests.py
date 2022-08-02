from deepdiff import DeepDiff

from config import path_config
from consts.json_fields import NOTES, EXTRA_FIELD
from tests.send_generated_input_script.data_generator import DataGenerator
from tests.test_base import TestBase


class DataTransformationTests(TestBase):
    def test_valid_input_generates_correct_output(self):
        generated_input = DataGenerator.generate_base_input_model()
        expected_output = DataGenerator.parse_base_output(generated_input)

        self.send_body(generated_input)
        actual_output = self.read_from_file(f"{path_config.TEST_STUDENTS_DIR_PATH}/{self.get_docs(expected_docs=1)[0]}")

        self.assertFalse(DeepDiff(expected_output, actual_output))

    def test_valid_input_with_notes_generates_correct_output(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[NOTES] = "test"
        expected_output = DataGenerator.parse_base_output(generated_input)
        expected_output[NOTES] = "test"

        self.send_body(generated_input)
        actual_output = self.read_from_file(f"{path_config.TEST_STUDENTS_DIR_PATH}/{self.get_docs(expected_docs=1)[0]}")

        self.assertFalse(DeepDiff(expected_output, actual_output))

    def test_valid_input_with_extra_field_generates_correct_output(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[EXTRA_FIELD] = "test"
        expected_output = DataGenerator.parse_base_output(generated_input)
        generated_input[EXTRA_FIELD] = "test"

        self.send_body(generated_input)
        actual_output = self.read_from_file(f"{path_config.TEST_STUDENTS_DIR_PATH}/{self.get_docs(expected_docs=1)[0]}")

        self.assertFalse(DeepDiff(expected_output, actual_output))
