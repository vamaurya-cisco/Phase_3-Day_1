# Worklist

A simple, business-oriented to-do web application built with Python and Flask.
Its single-page interface lets you add tasks, review upcoming work, and delete
tasks you no longer need.

## Features

- Add tasks with four required fields:
  - **Task name:** up to 200 characters.
  - **Priority:** High, Medium, or Low.
  - **Category:** Work, Personal, or Health.
  - **Due date:** selected with a date picker.
- View tasks in a table sorted by due date, earliest first.
- Delete a task using the button on its row.
- Use a responsive interface with CSS included directly in the HTML template.

Tasks are stored as dictionaries in an in-memory Python list. There is no
database, and all tasks are lost when the application stops or restarts,
including restarts triggered by the debug reloader. The list is shared across
visitors to the same application process; there are no user accounts or private
task lists.

## Requirements

- Python 3.9 or newer, with `pip` and virtual environment support.
- A web browser.

Flask and its dependencies are installed through [requirements.txt](requirements.txt).

## Setup

Open a terminal in the project directory.

### Linux or macOS

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you already have a virtual environment, activate it without recreating it.

### Install dependencies

With the virtual environment active, run:

```bash
python -m pip install -r requirements.txt
```

## Run the application

From the project directory, with the virtual environment active:

```bash
python app.py
```

Open **http://127.0.0.1:5000/** in your browser. Fill in all four fields and
select **Add task**. Use **Delete** on a row to remove that task.

Press `Ctrl+C` in the terminal to stop the server. When finished, leave the
virtual environment with:

```bash
deactivate
```

**Development only:** [app.py](app.py) starts Flask's development server with
debug mode enabled. Do not expose this server to the public internet or use it
for production deployment.

## Project files

- [app.py](app.py): Flask routes, input validation, and in-memory task storage.
- [templates/index.html](templates/index.html): Form, task table, and inline CSS.
- [requirements.txt](requirements.txt): Python dependency requirements.
