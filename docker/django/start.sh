#!/usr/bin/env bash

# wait for Postgres to start
function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="docker", user="docker", password="docker", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python manage.py migrate

gunicorn pft.wsgi:application -w 2 -b 0.0.0.0:8000 --reload

python manage.py runserver 0.0.0.0:8000