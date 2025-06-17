#!/bin/sh

# Wait for PostgreSQL to be ready before continuing
echo "⏳ Waiting for PostgreSQL to be ready..."

MAX_RETRIES=20
RETRY_INTERVAL=2
COUNTER=0

while ! pg_isready -d "$DATABASE_URL" > /dev/null 2>&1; do
  COUNTER=$((COUNTER + 1))
  echo "  ⏳ DB not ready yet... ($COUNTER/$MAX_RETRIES)"
  if [ "$COUNTER" -ge "$MAX_RETRIES" ]; then
    echo "❌ Failed to connect to DB after $MAX_RETRIES attempts. Exiting."
    exit 1
  fi
  sleep $RETRY_INTERVAL
done

echo "✅ PostgreSQL is ready!"
