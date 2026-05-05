#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding badges..."
python seed_badges.py

echo "Starting server..."
exec uvicorn config.asgi:application --host 0.0.0.0 --port 8080
