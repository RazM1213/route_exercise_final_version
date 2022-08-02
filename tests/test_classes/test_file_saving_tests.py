from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, NOTES
from tests.send_generated_input_script.data_generator import DataGenerator
from tests.test_base import TestBase


class FileSavingTests(TestBase):
    def test_valid_file_name_capitalized(self):
        generated_input = DataGenerator.generate_base_input_model()

        self.send_body(generated_input)

        self.assertEqual([f"{generated_input[STUDENT_DETAILS][FIRST_NAME].title()}_{generated_input[STUDENT_DETAILS][LAST_NAME].title()}.txt"], self.get_docs(expected_docs=1))

    def test_valid_file_name_hyphen_lastname(self):
        generated_input = DataGenerator.generate_base_input_model()

        generated_input[STUDENT_DETAILS][FIRST_NAME] = 'Test'
        generated_input[STUDENT_DETAILS][LAST_NAME] = 'Ben Test'

        self.send_body(generated_input)

        self.assertEqual(['Test_Ben-Test.txt'], self.get_docs(expected_docs=1))

    def test_body_with_notes_text_file_saved_success(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[NOTES] = "test"

        self.send_body(generated_input)

        self.assertEqual(1, len(self.get_docs(expected_docs=1)))
