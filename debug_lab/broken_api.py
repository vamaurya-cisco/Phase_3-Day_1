"""Local-only FastAPI app with intentional runtime errors."""

from fastapi import FastAPI

from .employee_data import EMPLOYEES, EMPLOYEES_BY_ID, Employee, SalaryRequest

app = FastAPI(title="Runtime Debugging Lab (Broken)")


@app.post("/annual-salary")
def annual_salary(payload: SalaryRequest):
    return {"summary": "Annual salary: " + payload.monthly_salary * 12}


@app.get("/employees/{employee_id}/department")
def employee_department(employee_id: int):
    return {"department": EMPLOYEES_BY_ID[employee_id].department}


@app.post("/average-salary")
def average_salary(salaries: list[int]):
    return {"average": sum(salaries) / len(salaries)}


@app.get("/salary/parse")
def parse_salary(value: str):
    return {"monthly_salary": int(value)}


@app.get("/employees/{employee_id}/email")
def employee_email(employee_id: int):
    return {"email": EMPLOYEES_BY_ID[employee_id].email_address}


@app.get("/employees/by-index/{index}")
def employee_by_index(index: int):
    return EMPLOYEES[index]


@app.post("/employees")
def validate_employee(payload: dict):
    return Employee.model_validate(payload)