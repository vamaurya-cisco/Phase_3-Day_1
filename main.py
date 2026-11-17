from fastapi import FastAPI

from database import Base, engine
from models import Department, Student
from college_management_api.routers.departments import router as departments_router
from college_management_api.routers.students import router as students_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Management System API")
app.include_router(departments_router)
app.include_router(students_router)


@app.get("/")
def get_status() -> dict[str, str]:
    return {"message": "College Management System API is running"}
