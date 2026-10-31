# Todo API

REST API for managing tasks, created with FastAPI. It uses MySQL as its database. SQLAlchemy is used for database interaction.

## Features
- Retrieve all tasks
- Retrieve a task by its ID
- Create new tasks
- Partially update existing tasks
- Delete tasks
- Validate request data
- Handle errors and return appropriate HTTP status codes
- Run automated tests using pytest

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- MySQL

## Requirements

Before starting, make sure that all the requirements are installed:

- [Python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- MySQL Server

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/dt3r/todo-fastapi
   ```

2. Go to the project directory:

   ```bash
   cd todo-api
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

## Configuration

Create `.env` file in root directory of project:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
DB_NAME=todo_db
TEST_DB_NAME=todo_test
```

Replace values to your own to connect to MySQL.

Create a MySQL database:

```sql
CREATE DATABASE todo_db;
CREATE DATABASE todo_test;
```

> `todo_db` is used for main app, `todo_test` is for tests so it doesn't affect the main database.

## Running the Project

Run a local server:

```bash
uv run uvicorn app.main:app --reload
```

After app started up, you can visit those URLs:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/{task_id}` | Get task by ID |
| POST | `/tasks/` | Create a new task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Testing

Run automated tests:

```bash
uv run pytest -v
```
The tests cover:
- Retrieving tasks
- Creating tasks
- Retrieving tasks by ID
- Updating tasks
- Partial updates
- Request validation
- Deleting tasks
- Handling requests for non-existent tasks

