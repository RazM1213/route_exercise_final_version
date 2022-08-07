import time

from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, ID, SUBJECT_GRADES, SUBJECT, GRADES, BIRTHDATE, AGE, GENDER, BEHAVIOUR_GRADE
from tests.data_generator import DataGenerator
from tests.test_base import TestBase


class InvalidFieldValueTests(TestBase):
    def test_invalid_value_first_name_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[STUDENT_DETAILS][FIRST_NAME] = "raz1"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_last_name_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[STUDENT_DETAILS][LAST_NAME] = "matzliah1"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_id_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[STUDENT_DETAILS][ID] = 3227175701

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_subject_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[SUBJECT_GRADES][0][SUBJECT] = "Test1"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_grades_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[SUBJECT_GRADES][0][GRADES] = [101, 90, 80]

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_birtdate_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[BIRTHDATE] = "30/02/2000"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_birthdate_format_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[BIRTHDATE] = "27.06.2000"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_age_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[AGE] = -1

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_gender_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[GENDER] = "invalid_gender"

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())

    def test_invalid_value_behaviour_grade_body(self):
        input_model = DataGenerator.generate_base_input_model()
        input_model[BEHAVIOUR_GRADE] = 11

        self.send_body(input_model)

        time.sleep(2)

        self.assertEqual(0, self.get_number_of_all_documents())
