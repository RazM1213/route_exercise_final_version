import time

from consts.json_fields import FIRST_NAME, LAST_NAME, ID, STUDENT_DETAILS, GRADES, SUBJECT_GRADES, BIRTHDATE, AGE, GENDER, BEHAVIOUR_GRADE, NOTES
from tests.data_generator import DataGenerator
from tests.test_base import TestBase


class InvalidFieldTypeTests(TestBase):
    def test_invalid_type_student_details_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS] = [{
            f"{FIRST_NAME}": "test",
            f"{LAST_NAME}": "tester",
            f"{ID}": 123456789
        }]

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_first_name_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][FIRST_NAME] = 1

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_last_name_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][LAST_NAME] = 1

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_id_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[STUDENT_DETAILS][ID] = "test"

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_subject_grades_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[SUBJECT_GRADES] = "test"

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_grades_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[SUBJECT_GRADES][0][GRADES] = 100

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_birthdate_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[BIRTHDATE] = 27062000

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_age_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[AGE] = "a"

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_gender_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[GENDER] = 1

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_behaviour_grade_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[BEHAVIOUR_GRADE] = "12"

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_type_notes_body(self):
        generated_input = DataGenerator.generate_base_input_model()
        generated_input[NOTES] = [1]

        self.send_body(generated_input)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())
