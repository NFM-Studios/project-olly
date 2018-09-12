#!/bin/bash

echo Current site is $site

echo Running Migrations.
python3 manage.py migrate --settings olly.$site"_settings"

echo Collecting static files
python3 manage.py collectstatic --noinput

echo Starting Gunicorn.
gunicorn olly.$site"_wsgi:application" \
    --bind unix:/sock/$site".sock" \
    --workers 3
