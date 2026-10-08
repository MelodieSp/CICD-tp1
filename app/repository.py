from .models import FieldEnum, Student
from .seed_data import SEED_STUDENTS


class StudentRepository:
    def __init__(self):
        self._students: list[Student] = []
        self._next_id = 1
        self.reset()

    def get(self, student_id: int) -> Student | None:
        return next((s for s in self._students if s.id == student_id), None)

    def get_by_email(self, email: str) -> Student | None:
        return next((s for s in self._students if s.email == email), None)

    def get_all(self):
        return self._students

    def get_all_by_field(self, field: FieldEnum) -> list[Student]:
        return list(filter(lambda s: s.field == field, self._students))

    def filter(self, query: str) -> list[Student]:
        query = query.lower()
        return list(filter(lambda s: query in s.firstName.lower() or query in s.lastName.lower(), self._students))

    def create(self, data: dict) -> Student:
        student = Student(id=self._next_id, **data)
        self._students.append(student)
        self._next_id += 1
        return student

    def update(self, student: Student, data: dict) -> Student | None:
        updated = Student(id=student.id, **data)
        idx = self._students.index(student)
        self._students[idx] = updated
        return updated

    def delete(self, student_id: int) -> bool:
        existing = self.get(student_id)
        if not existing:
            return False
        self._students.remove(existing)
        return True

    def reset(self):
        self._students = []
        self._next_id = 1
        for data in SEED_STUDENTS:
            self.create(data)
