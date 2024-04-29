#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn  --config /scripts/gunicorn_config.py chatbot.asgi:application
