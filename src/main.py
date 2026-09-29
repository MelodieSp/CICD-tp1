from fastapi import FastAPI

from src.repository import StudentRepository

app = FastAPI()
students = StudentRepository()


@app.get("/")
def root():
    return {"ok"}


@app.get("/students")
def get_students():
    return students.get_all()


@app.get("/students/:id")
def get_students():
    return students.get_all()
