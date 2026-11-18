from pydantic import BaseModel, Field


class Employee(BaseModel):
    name: str = Field(min_length=1)
    monthly_salary: int = Field(strict=True, gt=0)
    department: str = Field(min_length=1)
    email: str = Field(min_length=1)


class SalaryRequest(BaseModel):
    monthly_salary: int = Field(strict=True, gt=0)


EMPLOYEES = (
    Employee(name="Asha", monthly_salary=5000, department="Engineering", email="asha@example.com"),
    Employee(name="Jordan", monthly_salary=4500, department="Support", email="jordan@example.com"),
)
EMPLOYEES_BY_ID = dict(enumerate(EMPLOYEES, start=1))