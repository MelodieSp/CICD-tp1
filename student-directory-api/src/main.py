from fastapi import FastAPI
from src.repository import StudentRepository

app = FastAPI()
StudentRepository = StudentRepository()

@app.get("/")
def root():
    return {"ok"}

@app.get("/students")
def get_students():
    return StudentRepository.get_all()