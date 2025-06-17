# 🧠 Backend (Flask) — User Auth API

This is the Flask-based backend for the User Authentication system. It is containerized and works within the full stack provided via Docker Compose.

👉 **NOTE:** To run the full application stack (PostgreSQL, Redis, NGINX, Celery, etc.), use the main [`README.md`](../README.md) in the root directory.

---

## 📁 Project Structure (One-liners)

```
backend/
├── app/              # Main application package with blueprints, models, and configs
├── migrations/       # Alembic-generated DB migration files
├── tests/            # Pytest-based test suite
├── Dockerfile.dev    # Dev-only Dockerfile with hot reload and Poetry
├── entrypoint.sh     # Entrypoint to initialize config/migrations
└── pyproject.toml    # Poetry dependencies and tool config
```

---

## 🧪 Poetry Setup

We use [Poetry](https://python-poetry.org/) for dependency management.

### 📦 Install Poetry (if not already)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

> Or use pipx: `pipx install poetry`

### 📥 Install dependencies

```bash
cd backend
poetry install
```

---

## ⚙️ Local Environment Setup (`.env.local`)

Create a `.env.local` file in the `backend/` folder to override Docker service names and use `localhost` when running the app directly (outside Docker):

```env
FLASK_APP=app:create_app
CONFIG_NAME=development
FLASK_DEBUG=1

# Local PostgreSQL (if running locally)
DATABASE_URL=postgresql://flask_user:flask_password@localhost:5432/flask_dev_db

# Local Redis
REDIS_URL=redis://localhost:6379/0

# Secrets
SECRET_KEY=your-dev-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

> You can copy from `.env.dev`:\
> `cp .env.dev .env.local` and then update `localhost` as needed.

---

## 🦠 Database Migration Commands

```bash
# 1. Initialize migrations folder
flask --env-file .env.local db init

# 2. Create a migration if needed
flask --env-file .env.local db migrate -m "Initial migration"

# 3. Apply the migration
flask --env-file .env.local db upgrade
```

---

## 🚀 Run the Flask Server Locally (without Docker)

```bash
cd backend
flask --env-file .env.local run -h 0.0.0.0 -p 8000
```

Server will be available at:\
👉 [http://localhost:8000](http://localhost:8000)

---

## 💪 Run Test Cases

To run all tests:

```bash
cd backend
poetry shell
pytest
```

Or in one shot without a shell:

```bash
poetry run pytest
```

---

## 🔌 API Endpoints

| Method | Endpoint                     | Description                        |
| ------ | -----------------------------| ---------------------------------- |
| POST   | `/auth/register`             | Register new user                  |
| POST   | `/auth/login`                | Log in and get tokens              |
| POST   | `/auth/logout`               | Log out (revoke access token)      |
| POST   | `/auth/refresh`              | Refresh access token               |
| GET    | `/auth/me`                   | Get current user profile           |
| GET    | `/api/v1/health`             | Health check endpoint              |
| GET    | `/api/v1/users`              | Get all users                      |
| GET    | `/api/v1/users/<user_id>`    | Health check endpoint              |

---
