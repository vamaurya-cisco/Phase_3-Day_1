from connection import getSqliteConnection


def main():
    connection = getSqliteConnection()
    try:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("DROP TABLE IF EXISTS students")
            connection.execute("DROP TABLE IF EXISTS departments")
            connection.execute(
                """
                CREATE TABLE departments (
                    DepartmentId INTEGER PRIMARY KEY,
                    DepartmentName TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE students (
                    StudentId INTEGER PRIMARY KEY,
                    StudentName TEXT NOT NULL,
                    DepartmentId INTEGER,
                    FOREIGN KEY (DepartmentId)
                        REFERENCES departments (DepartmentId)
                )
                """
            )
            departments = connection.executemany(
                "INSERT INTO departments (DepartmentId, DepartmentName) VALUES (?, ?)",
                [
                    (1, "Computer Science"),
                    (2, "Electrical Engineering"),
                    (3, "Mechanical Engineering"),
                    (4, "Mathematics"),
                    (5, "Physics"),
                ],
            ).rowcount
            students = connection.executemany(
                """
                INSERT INTO students (StudentId, StudentName, DepartmentId)
                VALUES (?, ?, ?)
                """,
                [
                    (101, "Alice Johnson", 1),
                    (102, "Bob Smith", 2),
                    (103, "Carol Lee", 3),
                    (104, "David Brown", 4),
                    (105, "Emily White", 5),
                ],
            ).rowcount
    finally:
        connection.close()

    print(f"Inserted {departments} rows into departments.")
    print(f"Inserted {students} rows into students.")


if __name__ == "__main__":
    main()
