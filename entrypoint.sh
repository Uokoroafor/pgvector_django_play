#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status.

echo "Checking for .env file..."
python generate_env.py

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn my_app.wsgi:application --bind 0.0.0.0:8000