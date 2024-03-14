#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "en attente de PostGres"
    sleep 1
done

# effectuer les migrations
echo "effectuer les migrations de la BDD..."

python manage.py makemigrations && python manage.py mirgate

python manage.py collectstatic --no-input

echo "lancer le server"

# LOCAL
# python manage.py runserver 0.0.0.0:8000

# PROD
gunicorn us_sba.wsgi:application  --workers=1 --bind=0.0.0.0:8000 --reload
