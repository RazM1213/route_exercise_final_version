from datetime import datetime

from consts.formats import DATETIME_FORMAT
from mappings.gender_mapping import gender_mapping
from models.input import Input
from models.output import Output
from models.output_student_details import OutputStudentDetails
from models.output_subject_grades import OutputSubjectGrades
from transform.transformer import Transformer


class StudentTransformer(Transformer):
    def parse_output(self, json_input) -> Output:
        student_input = Input(**json_input)
        return Output(
            self.parse_student_details(student_input),
            self.parse_subject_grades(student_input),
            self.parse_total_avg(student_input),
            self.parse_birthdate(student_input),
            student_input.age,
            self.parse_gender(student_input),
            self.parse_is_good_behaviour(student_input),
            student_input.notes if student_input.notes is not None else None
        )

    @staticmethod
    def parse_student_details(student_input):
        first_name = student_input.studentDetails.firstName
        last_name = student_input.studentDetails.lastName
        id = student_input.studentDetails.id
        full_name = first_name + " " + last_name
        return OutputStudentDetails(first_name, last_name, full_name, id)

    @staticmethod
    def parse_subject_grades(student_input):
        subjects_avg = []
        for subject in student_input.subjectGrades:
            subject_name = subject.subject
            if len(subject.grades):
                avg = sum(subject.grades) / len(subject.grades)
            else:
                avg = None
            subject_avg = OutputSubjectGrades(subject_name, avg)
            subjects_avg.append(subject_avg)
        return subjects_avg

    @staticmethod
    def parse_birthdate(student_input):
        birth_date = datetime.strptime(student_input.birthDate, DATETIME_FORMAT)
        if birth_date.year > 2000:
            birth_date_str = f"{birth_date.day}/{birth_date.month}/{birth_date.year - 2000}"
        else:
            birth_date_str = f"{birth_date.day}/{birth_date.month}/{birth_date.year - 1900}"
        return birth_date_str

    @staticmethod
    def parse_gender(student_input):
        return gender_mapping[student_input.gender]

    @staticmethod
    def parse_is_good_behaviour(student_input):
        if student_input.behaviourGrade >= 5:
            return True
        return False

    def parse_total_avg(self, student_input):
        sum = 0
        for subject in self.parse_subject_grades(student_input):
            sum += subject.avg
        return sum / len(self.parse_subject_grades(student_input))
