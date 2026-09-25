from enum import StrEnum
from pydantic import BaseModel, EmailStr, Field

class FieldEnum(StrEnum):
    INFORMATIQUE = "informatique"
    MATHEMATIQUES = "mathématiques"
    PHYSIQUE = "physique"
    CHIMIE = "chimie"


class StudentsBase(BaseModel):
    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)
    field: FieldEnum

class Student(StudentsBase):
    id: int

class StudentCreate(StudentsBase):
    pass
class StudentUpdate(StudentsBase):
    pass