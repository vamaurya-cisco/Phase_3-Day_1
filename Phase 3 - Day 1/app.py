"""Serve a single-page Flask to-do app with process-local, in-memory tasks.

Tasks contain a name, priority, category, and due date and are lost on restart.
"""

from datetime import date

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

tasks = []


@app.get("/")
def index():
    """Render the task page in ascending due-date order.

    Returns:
        str: Rendered HTML containing the sorted tasks and their list indices.
    """
    # Keep original list indices so deletion targets the correct sorted row.
    sorted_tasks = sorted(enumerate(tasks), key=lambda item: item[1]["due_date"])
    return render_template("index.html", tasks=sorted_tasks)


@app.post("/tasks")
def add_task():
    """Validate submitted form fields and append a task to the in-memory list.

    Returns:
        flask.Response: A redirect to the task page after adding the task.

    Raises:
        werkzeug.exceptions.BadRequest: If a required field is missing or invalid.
    """
    task = request.form.get("task", "").strip()
    priority = request.form.get("priority", "")
    category = request.form.get("category", "")
    due_date = request.form.get("due_date", "")

    if not task or len(task) > 200:
        abort(400, description="Task name is required and must be 200 characters or fewer.")
    if priority not in ("High", "Medium", "Low"):
        abort(400, description="Choose a priority: High, Medium, or Low.")
    if category not in ("Work", "Personal", "Health"):
        abort(400, description="Choose a category: Work, Personal, or Health.")
    try:
        due_date = date.fromisoformat(due_date).isoformat()
    except ValueError:
        abort(400, description="A valid due date is required.")

    tasks.append({
        "task": task,
        "priority": priority,
        "category": category,
        "due_date": due_date,
    })
    return redirect(url_for("index"))


@app.post("/tasks/<int:task_index>/delete")
def delete_task(task_index):
    """Delete the task at its original in-memory list index.

    Args:
        task_index (int): Zero-based index of the task to remove.

    Returns:
        flask.Response: A redirect to the task page after deleting the task.

    Raises:
        werkzeug.exceptions.NotFound: If the index is beyond the task list.
    """
    if task_index >= len(tasks):
        abort(404, description="Task not found.")
    tasks.pop(task_index)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
