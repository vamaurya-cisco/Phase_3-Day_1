from datetime import datetime
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log to both the terminal and logs/application.log.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "application.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger("ai_log_analysis")
app = FastAPI(title="AI Log Analysis Demo", version="1.0.0")

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "AI Log Analysis Demo is running"}

@app.get("/health")
def health():
    logger.info("Health check successful")
    return {"status": "healthy"}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    # Demo data only; replace with a database in a real application.
    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"},
    }

    employee = employees.get(employee_id)
    if employee is None:
        logger.error("EmployeeNotFound: employee_id=%s", employee_id)
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee %s fetched successfully", employee_id)
    return employee

@app.get("/employees/{employee_id}/bonus")
def calculate_bonus(employee_id: int):
    employees = {
        101: {"name": "Rahul", "salary": 50000.0},
        102: {"name": "Priya", "salary": 60000.0},
    }

    employee = employees.get(employee_id)
    if employee is None:
        logger.error("EmployeeNotFound: employee_id=%s", employee_id)
        raise HTTPException(status_code=404, detail="Employee not found")

    bonus = employee["salary"] * 0.10
    logger.info("Bonus calculated for employee_id=%s", employee_id)
    return {"employee_id": employee_id, "bonus": bonus}

@app.get("/demo-log-errors")
def generate_demo_errors():
    """Write representative demo errors to the runtime log.
    This endpoint deliberately logs error patterns for the Copilot exercise.
    It does not deliberately crash the API.
    """
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.warning("Slow database response: 8 seconds")
    logger.error("ValueError: Invalid employee salary value")
    logger.error("ValueError: Invalid employee salary value")
    logger.error("TimeoutError: External payment API request timed out")
    logger.error("TimeoutError: External payment API request timed out")
    logger.warning("Payment API response delayed")
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.error("KeyError: Employee ID not found")
    logger.error("ZeroDivisionError: Division by zero")
    logger.warning("High API response time detected")


    logger.info("Demo error patterns generated")
    return {
        "message": "Demo log patterns written",
        "log_file": str(LOG_DIR / "application.log"),
    }
