from datetime import datetime
from typing import Optional, List

import pydantic

from consts.formats import DATETIME_FORMAT
from consts.json_fields import BIRTHDATE, AGE, GENDER, BEHAVIOUR_GRADE
from custom_exceptions.age_format_exception import AgeFormatException
from custom_exceptions.behaviour_grade_format_exception import BehaviourGradeFormatException
from custom_exceptions.date_format_exception import DateFormatException
from custom_exceptions.gender_format_exception import GenderFormatException
from mappings.gender_mapping import gender_mapping
from models.input_student_details import InputStudentDetails
from models.input_subject_grades import InputSubjectGrades


class Input(pydantic.BaseModel):
    studentDetails: InputStudentDetails
    subjectGrades: List[InputSubjectGrades]
    birthDate: str
    age: int
    gender: str
    behaviourGrade: int
    notes: Optional[str]

    @pydantic.validator(BIRTHDATE)
    def validate_birthdate(cls, value):
        try:
            datetime.strptime(str(value), DATETIME_FORMAT)
        except ValueError:
            raise DateFormatException(value=value, message=f"Invalid date format. ({value})")
        return value

    @pydantic.root_validator
    def validate_age(cls, values: dict):
        if (datetime.now() - datetime.strptime(values[BIRTHDATE], DATETIME_FORMAT)).days // 365 != values[AGE]:
            raise AgeFormatException(value=values[AGE], message=f"Age does not match birth date. ({values[AGE]}) ({values[BIRTHDATE]})")
        return values

    @pydantic.validator(GENDER)
    def validate_gender(cls, value):
        if value not in gender_mapping.keys():
            raise GenderFormatException(value=value, message=f"Gender must be זכר/נקבה/אחר ({value})")
        return value

    @pydantic.validator(BEHAVIOUR_GRADE)
    def validate_behaviour_grade(cls, value):
        if value < 1 or value > 10:
            raise BehaviourGradeFormatException(value=value, message=f"Behaviour grade must be between 1 and 10. ({value})")
        return value
