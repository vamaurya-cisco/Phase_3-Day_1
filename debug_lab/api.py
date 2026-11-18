from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Path

from .employee_data import EMPLOYEES, EMPLOYEES_BY_ID, Employee, SalaryRequest

app = FastAPI(title="Runtime Debugging Lab (Fixed)")


def get_employee(employee_id: int) -> Employee:
    employee = EMPLOYEES_BY_ID.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/annual-salary")
def annual_salary(payload: SalaryRequest):
    annual = payload.monthly_salary * 12
    return {"summary": f"Annual salary: {annual}"}


@app.get("/employees/{employee_id}/department")
def employee_department(employee_id: int):
    return {"department": get_employee(employee_id).department}


@app.post("/average-salary")
def average_salary(salaries: Annotated[list[int], Body(min_length=1)]):
    return {"average": sum(salaries) / len(salaries)}


@app.get("/salary/parse")
def parse_salary(value: str):
    try:
        salary = int(value)
    except ValueError as error:
        raise HTTPException(status_code=422, detail="Salary must be a positive integer") from error
    if salary <= 0:
        raise HTTPException(status_code=422, detail="Salary must be a positive integer")
    return {"monthly_salary": salary}


@app.get("/employees/{employee_id}/email")
def employee_email(employee_id: int):
    return {"email": get_employee(employee_id).email}


@app.get("/employees/by-index/{index}")
def employee_by_index(index: Annotated[int, Path(ge=0)]) -> Employee:
    if index >= len(EMPLOYEES):
        raise HTTPException(status_code=404, detail="Employee index not found")
    return EMPLOYEES[index]


@app.post("/employees")
def validate_employee(payload: Employee) -> Employee:
    return payload