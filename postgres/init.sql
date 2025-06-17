DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'flask_dev_db') THEN
        CREATE DATABASE flask_dev_db;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'flask_db') THEN
        CREATE DATABASE flask_db;
    END IF;
END $$;

-- Create user if not exists (PostgreSQL doesn't support IF NOT EXISTS for users directly)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'flask_user') THEN
        CREATE USER flask_user WITH PASSWORD 'flask_password';
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE flask_dev_db TO flask_user;
GRANT ALL PRIVILEGES ON DATABASE flask_db TO flask_user;

-- Enable extensions
\c flask_dev_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c flask_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
