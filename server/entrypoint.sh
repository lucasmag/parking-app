#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

echo "Enabling PostGIS extension..."
PGPASSWORD=postgres psql -h db -U postgres -d parking_app -c "CREATE EXTENSION IF NOT EXISTS postgis;"
PGPASSWORD=postgres psql -h db -U postgres -d parking_app -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"

# Run migrations
echo "Running migrations..."
cd /app/src
uv run python manage.py makemigrations user
uv run python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
uv run python manage.py shell << END
import os
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        first_name='Admin',
        last_name='User',
        password='admin'
    )
    print('Superuser created: admin@example.com / admin')
else:
    print('Superuser already exists')
END

# Collect static files
echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --noinput

# Start server
echo "Starting Django server..."
cd /app
exec "$@"