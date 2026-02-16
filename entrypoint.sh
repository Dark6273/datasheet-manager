#!/bin/sh
set -e

python manage.py migrate --noinput

exec gunicorn datasheet.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout ${GUNICORN_TIMEOUT:-120}
