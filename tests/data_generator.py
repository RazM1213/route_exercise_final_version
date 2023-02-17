import datetime
import random
import string

from consts import formats
from consts.consts import GOOD_BEHAVIOUR_BOUNDARY, INPUT_MALE, INPUT_FEMALE, INPUT_OTHER
from consts.formats import DATETIME_FORMAT, ELASTIC_DATETIME_FORMAT
from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, SUBJECT_GRADES, GRADES, GENDER, BEHAVIOUR_GRADE, ID, SUBJECT, BIRTHDATE, AGE, FULLNAME, AVERAGE, TOTAL_AVERAGE, IS_GOOD_BEHAVIOUR, NOTES
from mappings.gender_mapping import gender_mapping


class DataGenerator:
    @staticmethod
    def generate_base_input_model() -> dict:
        birth_date = DataGenerator.generate_birth_date()

        return {
            STUDENT_DETAILS: {
                FIRST_NAME: DataGenerator.generate_name(),
                LAST_NAME: DataGenerator.generate_name(),
                ID: DataGenerator.generate_id()
            },
            SUBJECT_GRADES: [
                {
                    SUBJECT: DataGenerator.generate_name(),
                    GRADES: DataGenerator.generate_grades()
                }
            ],
            BIRTHDATE: birth_date,
            AGE: DataGenerator.calculate_age(birth_date),
            GENDER: DataGenerator.generate_gender(),
            BEHAVIOUR_GRADE: DataGenerator.generate_behaviour_grade()
        }

    @staticmethod
    def parse_output(generated_input: dict) -> dict:
        subject_grades = [{SUBJECT: subject[SUBJECT],
                           AVERAGE: sum(subject[GRADES]) / len(subject[GRADES]) if len(subject[GRADES]) else 0}
                          for subject in generated_input[SUBJECT_GRADES]]

        total_average = 0
        for subject in subject_grades:
            total_average += subject[AVERAGE] / len(subject_grades) if subject[AVERAGE] else 0

        output_dict = {
            STUDENT_DETAILS: {
                FIRST_NAME: generated_input[STUDENT_DETAILS][FIRST_NAME],
                LAST_NAME: generated_input[STUDENT_DETAILS][LAST_NAME],
                FULLNAME: f"{generated_input[STUDENT_DETAILS][FIRST_NAME]} {generated_input[STUDENT_DETAILS][LAST_NAME]}",
                ID: generated_input[STUDENT_DETAILS][ID]
            },
            SUBJECT_GRADES: subject_grades,
            TOTAL_AVERAGE: total_average,
            BIRTHDATE: datetime.datetime.strftime(datetime.datetime.strptime(generated_input[BIRTHDATE], DATETIME_FORMAT), ELASTIC_DATETIME_FORMAT),
            AGE: generated_input[AGE],
            GENDER: gender_mapping[generated_input[GENDER]],
            IS_GOOD_BEHAVIOUR: generated_input[BEHAVIOUR_GRADE] >= GOOD_BEHAVIOUR_BOUNDARY
        }

        if NOTES in generated_input.keys():
            output_dict[NOTES] = generated_input[NOTES]

        return output_dict

    @staticmethod
    def generate_name() -> str:
        return "".join(random.choices(string.ascii_uppercase, k=8))

    @staticmethod
    def generate_id() -> int:
        return random.randint(111111111, 999999999)

    @staticmethod
    def generate_grades() -> list:
        return [random.randint(1, 100) for grade in range(3)]

    @staticmethod
    def generate_birth_date() -> str:
        return datetime.datetime(random.randint(1900, 2010), random.randint(1, 10), random.randint(1, 28)).strftime(formats.DATETIME_FORMAT)

    @staticmethod
    def calculate_age(birth_date) -> int:
        return (datetime.datetime.now() - datetime.datetime.strptime(birth_date, formats.DATETIME_FORMAT)).days // 365

    @staticmethod
    def generate_gender() -> str:
        return random.choice([INPUT_MALE, INPUT_FEMALE, INPUT_OTHER])

    @staticmethod
    def generate_behaviour_grade() -> int:
        return random.randint(1, 10)
