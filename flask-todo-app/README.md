# Flask Todo App

A small, clean Flask web application for managing a todo list — built with
the application factory pattern, SQLAlchemy, and a simple JSON API alongside
the HTML frontend.

## Features

- Add, complete/uncomplete, and delete todos
- Persisted to a local SQLite database
- Minimal, responsive HTML/CSS frontend (no JS framework required)
- JSON API endpoints under `/api/todos` for programmatic access

## Project structure

```
flask-todo-app/
├── app/
│   ├── __init__.py        # Application factory
│   ├── models.py          # SQLAlchemy models
│   ├── routes.py          # Routes / views (blueprint)
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
├── instance/               # Local SQLite DB lives here (gitignored)
├── tests/
│   └── test_app.py
├── config.py               # App configuration
├── run.py                  # Entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# 1. Clone your repo and cd into it
git clone <your-repo-url>
cd flask-todo-app

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

## API

| Method | Endpoint             | Description         |
|--------|-----------------------|----------------------|
| GET    | `/api/todos`           | List all todos       |
| POST   | `/api/todos`           | Create a todo (`{"title": "..."}`) |
| DELETE | `/api/todos/<id>`      | Delete a todo        |

## Running tests

```bash
pip install pytest
pytest
```

## Pushing to your existing GitHub repo

From inside this project folder:

```bash
git init                     # skip if the repo is already initialized
git add .
git commit -m "Initial commit: Flask todo app"
git branch -M main
git remote add origin <your-repo-url>   # skip if remote already set
git push -u origin main
```

## Deployment notes

For production, set a real `SECRET_KEY` and, if you want something more
robust than SQLite, point `DATABASE_URL` at a Postgres/MySQL instance:

```bash
export SECRET_KEY="a-long-random-string"
export DATABASE_URL="postgresql://user:pass@host/dbname"
```

Then run with a production WSGI server, e.g.:

```bash
pip install gunicorn
gunicorn "app:create_app()"
```
