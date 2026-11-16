from flask import Flask, jsonify

from connection import getSqliteConnection


app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({"endpoints": ["/studentDepartments", "/departments"]})


@app.get("/studentDepartments")
def student_departments():
    connection = getSqliteConnection()
    try:
        rows = connection.execute(
            """
            SELECT students.StudentName, departments.DepartmentName
            FROM students
            LEFT JOIN departments
                ON students.DepartmentId = departments.DepartmentId
            ORDER BY students.StudentId
            """
        ).fetchall()
    finally:
        connection.close()

    return jsonify([
        {"studentName": student_name, "departmentName": department_name}
        for student_name, department_name in rows
    ])


@app.get("/departments")
def departments():
    connection = getSqliteConnection()
    try:
        rows = connection.execute(
            """
            SELECT DepartmentId, DepartmentName
            FROM departments
            ORDER BY DepartmentId
            """
        ).fetchall()
    finally:
        connection.close()

    return jsonify([
        {"DepartmentId": department_id, "DepartmentName": department_name}
        for department_id, department_name in rows
    ])


if __name__ == "__main__":
    app.run(debug=True)
