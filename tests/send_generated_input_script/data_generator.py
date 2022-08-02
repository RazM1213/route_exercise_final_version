import datetime
import random
import string

from consts import formats, strings
from consts.formats import DATETIME_FORMAT
from consts.json_fields import STUDENT_DETAILS, FIRST_NAME, LAST_NAME, SUBJECT_GRADES, GRADES, GENDER, BEHAVIOUR_GRADE, ID, SUBJECT, BIRTHDATE, AGE
from mappings.gender_mapping import gender_mapping


class DataGenerator:
    @staticmethod
    def generate_base_input_model() -> dict:
        first_name = DataGenerator.generate_name()
        last_name = DataGenerator.generate_name()
        id = DataGenerator.generate_id()
        subject = DataGenerator.generate_name()
        grades = DataGenerator.generate_grades()
        birth_date = DataGenerator.generate_birth_date()
        age = DataGenerator.calculate_age(birth_date)
        gender = DataGenerator.generate_gender()
        behaviour_grade = DataGenerator.generate_behaviour_grade()

        return {
            "studentDetails": {
                "firstName": first_name,
                "lastName": last_name,
                "id": id
            },
            "subjectGrades": [
                {
                    "subject": subject,
                    "grades": grades
                }
            ],
            "birthDate": birth_date,
            "age": age,
            "gender": gender,
            "behaviourGrade": behaviour_grade
        }

    @staticmethod
    def parse_base_output(generated_input: dict) -> dict:
        fullname = f"{generated_input[STUDENT_DETAILS][FIRST_NAME]} {generated_input[STUDENT_DETAILS][LAST_NAME]}"
        if len(generated_input[SUBJECT_GRADES][0][GRADES]):
            average = sum(generated_input[SUBJECT_GRADES][0][GRADES]) / len(generated_input[SUBJECT_GRADES][0][GRADES])
        else:
            average = None
        gender = gender_mapping[generated_input[GENDER]]
        is_good_behaviour = generated_input[BEHAVIOUR_GRADE] >= 5
        total_average = average
        birth_date = datetime.datetime.strptime(generated_input[BIRTHDATE], DATETIME_FORMAT)

        if birth_date.year > 2000:
            birth_date_str = f"{birth_date.day}/{birth_date.month}/{birth_date.year - 2000}"
        else:
            birth_date_str = f"{birth_date.day}/{birth_date.month}/{birth_date.year - 1900}"

        return {
            "studentDetails": {
                "firstName": generated_input[STUDENT_DETAILS][FIRST_NAME],
                "lastName": generated_input[STUDENT_DETAILS][LAST_NAME],
                "fullName": fullname,
                "id": generated_input[STUDENT_DETAILS][ID]
            },
            "subjectGrades": [
                {
                    "subject": generated_input[SUBJECT_GRADES][0][SUBJECT],
                    "avg": average
                }
            ],
            "totalAvg": total_average,
            "birthDate": birth_date_str,
            "age": generated_input[AGE],
            "gender": gender,
            "isGoodBehaviour": is_good_behaviour
        }

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
        return random.choice([strings.INPUT_MALE, strings.INPUT_FEMALE, strings.INPUT_OTHER])

    @staticmethod
    def generate_behaviour_grade() -> int:
        return random.randint(1, 10)
