from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Department, Student
from schemas import StudentCreate, StudentOut


router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)) -> list[Student]:
    statement = select(Student).options(selectinload(Student.department))
    return list(db.scalars(statement).all())


@router.post(
    "/",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
) -> Student:
    department = db.get(Department, student.department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    db_student = Student(**student.model_dump())
    db_student.department = department
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
