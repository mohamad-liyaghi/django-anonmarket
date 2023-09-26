#!/bin/bash

echo "Apply database migrations"

python manage.py makemigrations
python manage.py migrate

echo "Collecting statis files"
python manage.py collectstatic --noinput

echo "Running the server"
gunicorn config.wsgi:application --bind 0.0.0.0:8000