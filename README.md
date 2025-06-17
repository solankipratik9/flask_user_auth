# Flask User Auth Project

A production-ready Flask application with PostgreSQL, Redis, Celery, and NGINX, built for scalable user authentication systems. This project supports both development and production environments using Docker Compose.

---

## 📂 Project Structure

```
.
├── backend/                # Flask application code
│   ├── app/                # Application package
│   ├── scripts/            # Entrypoint and DB wait scripts
│   ├── .env                # Prod environment config
│   ├── .env.dev            # Dev environment config
│   ├── Dockerfile          # Production image
│   ├── Dockerfile.dev      # Development image
├── nginx/                 # NGINX reverse proxy configuration
├── postgres/              # Init SQL for Postgres DB
├── docker-compose.yml     # Production Docker Compose file
├── docker-compose.dev.yml # Development Docker Compose file
├── .env                   # Production environment config
├── .env.dev               # Development environment config
```

---

## 💡 Development Environment

### .env.dev

```ini
POSTGRES_DB=flask_dev_db
POSTGRES_USER=flask_user
POSTGRES_PASSWORD=flask_password
DATABASE_URL=postgresql://flask_user:flask_password@postgres:5432/flask_dev_db

CONFIG_NAME=development
FLASK_APP=app:create_app
FLASK_DEBUG=1
REDIS_URL=redis://redis:6379/0
RATELIMIT_STORAGE_URL="memory://"
SECRET_KEY=your-dev-secret-key-here
JWT_SECRET_KEY=your-jwt-dev-secret-key-here
```

---

### ▶️ Start Dev Stack
```bash
docker compose --env-file .env.dev -f docker-compose.dev.yml build
docker compose --env-file .env.dev -f docker-compose.dev.yml up
```

### ⏹️ Stop Dev Stack
```bash
docker compose --env-file .env.dev -f docker-compose.dev.yml down -v
```

### 📁 List Database Tables (Dev)
```bash
docker compose --env-file .env.dev -f docker-compose.dev.yml exec postgres \
    psql -U flask_user -d flask_dev_db -c "\l"
```

---

## 🚀 Production Environment

### .env

```ini
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=

CONFIG_NAME=production
FLASK_APP=app:create_app
REDIS_URL=
RATELIMIT_STORAGE_URL=
SECRET_KEY=your-prod-secret-key
JWT_SECRET_KEY=your-jwt-prod-secret-key
```

---

### ▶️ Start Production Stack
```bash
docker compose up --build
```

### ⏹️ Stop Production Stack
```bash
docker compose down
```

---

## 🔧 Notes
- Ensure Docker and Docker Compose are installed on your system.
- Use `.env.dev` for development and `.env` for production.
- Production runs Gunicorn behind NGINX.
- Redis and Celery are used for background task processing.
- Flask-Migrate and Alembic handle DB migrations.

---

## 🔗 Related Docs
- See [Backend README](backend/readme.md) for more backend-specific info.

---

MIT License © 2025 Pratik Solanki
