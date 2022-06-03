#!/bin/sh
python manage.py collectstatic
python manage.py migrate
python manage.py migrate --run-syncdb
gunicorn learnify_cfg.wsgi:application --bind 0.0.0.0:8000