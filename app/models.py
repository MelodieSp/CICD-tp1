from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class FieldEnum(StrEnum):
    INFORMATIQUE = "informatique"
    MATHEMATIQUES = "mathématiques"
    PHYSIQUE = "physique"
    CHIMIE = "chimie"


class Student(BaseModel):
    id: int
    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)
    field: FieldEnum
