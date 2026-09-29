from src.models import Student, StudentCreate, StudentUpdate
from src.seed_data import SEED_STUDENTS


class StudentRepository:
    def __init__(self):
        self._students: list[Student] = []
        self._next_id = 1
        self._seed()

    def get(self, student_id: int) -> Student | None:
        return next((s for s in self._students if s.id == student_id), None)

    def get_all(self):
        return self._students

    def create(self, data: StudentCreate) -> Student:
        student = Student(id=self._next_id, **data.model_dump())
        self._students.append(student)
        self._next_id += 1
        return student

    def update(self, student_id: int, data: StudentUpdate) -> Student | None:
        existing = self.get(student_id)
        if not existing:
            return None
        updated = Student(id=student_id, **data.model_dump())
        idx = self._students.index(existing)
        self._students[idx] = updated
        return updated

    def delete(self, student_id: int) -> bool:
        existing = self.get(student_id)
        if not existing:
            return False
        self._students.remove(existing)
        return True

    def _seed(self):
        self._students = []
        self._next_id = 1
        for data in SEED_STUDENTS:
            self._students.append(Student(id=self._next_id, **data))
            self._next_id += 1

    def reset(self):
        self._seed()