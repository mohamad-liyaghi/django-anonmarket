#!/bin/bash

echo "Apply database migrations and run"
python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && pip install gunicorn && gunicorn config.wsgi:application --bind 0.0.0.0:8000