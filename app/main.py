from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError

from .models import FieldEnum, Student
from .repository import StudentRepository

app = FastAPI()
students = StudentRepository()


@app.get("/")
def root():
    return {"ok"}


@app.get("/students")
def get_students():
    return students.get_all()


@app.get("/students/stats")
def get_students_stats():
    all_students = students.get_all()

    total_students = len(all_students)
    average_grade = round(sum([student.grade for student in all_students]) / total_students, 2)
    students_by_field = {field: len(students.get_all_by_field(field)) for field in FieldEnum}
    best_student = max(all_students, key=lambda s: s.grade)

    return {
        "totalStudents": total_students,
        "averageGrade": average_grade,
        "studentsByField": students_by_field,
        "bestStudent": best_student,
    }


@app.get("/students/search")
def search_student(q: str | None = None):
    if not q:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No search query specified")
    return students.filter(q)


@app.get("/students/{id}")
def get_student(id):
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid student ID")
    student = students.get(id)
    if student:
        return student
    raise HTTPException(status.HTTP_404_NOT_FOUND, "No student exist with such ID")


@app.post("/students")
def create_student(data: dict):
    required_keys = set(Student.model_fields.keys()).difference({"id"})
    if not required_keys.issubset(set(data.keys())):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "All fields are required")
    if students.get_by_email(data["email"]) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "This email already exists")
    try:
        new_student = students.create(data)
        return new_student
    except ValidationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, [error["msg"] for error in e.errors()])


@app.put("/students/{id}")
def edit_student(id, data: dict):
    try:
        id = int(id)
    except ValueError:
        pass
    student = students.get(id)
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No student exist with such ID")

    existing_student = students.get_by_email(data["email"])
    if existing_student is not None and existing_student.id != id:
        raise HTTPException(status.HTTP_409_CONFLICT, "This email already exists")

    try:
        updated_student = students.update(student, data)
        return updated_student
    except ValidationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, [error["msg"] for error in e.errors()])


@app.delete("/students/{id}")
def delete_student(id):
    try:
        id = int(id)
    except ValueError:
        pass
    deleted = students.delete(id)
    if deleted:
        return f"Student with id {id} deleted successfully"
    raise HTTPException(status.HTTP_404_NOT_FOUND, "No student exist with such ID")
