#!/bin/bash

echo Current site is $site

echo Debug is $debug

echo Running Migrations.
python3 manage.py migrate --settings olly.$site"_settings"

echo creating a superuser.
python3 manage.py shell --settings olly.$site"_settings" -c "from django.contrib.auth.models import User; User.objects.create_superuser('NFMStudios', 'nfm.studios@gmail.com', 'Bigcatparadise!')"

echo Collecting static files
python3 manage.py collectstatic --noinput

echo Starting Gunicorn.
gunicorn olly.$site"_wsgi:application" \
    --bind unix:/sock/$site".sock" \
    --workers 2
