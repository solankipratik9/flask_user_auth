#!/bin/sh
set -e

# Wait for DB to be available
/app/scripts/wait-for-db.sh

# Check configuration using Python script
echo "🔎 Checking required environment variables..."
python /app/scripts/check_config.py

# Apply migrations
echo "📈 Running migrations..."
flask db upgrade

# Launch based on config
CONFIG_NAME=${CONFIG_NAME:-development}
echo "🌍 Environment: $CONFIG_NAME"

if [ "$CONFIG_NAME" = "production" ]; then
  echo "🚀 Starting Gunicorn (Production Mode)"
  exec gunicorn --bind 0.0.0.0:5000 \
                --workers 4 \
                --timeout 120 \
                --access-logfile - \
                --error-logfile - \
                wsgi:app
else
  echo "🚀 Starting Flask Development Server"
  exec flask run --host=0.0.0.0
fi
