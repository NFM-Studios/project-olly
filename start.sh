#!/bin/bash
echo Debug is $debug

echo Running Migrations.
python3 manage.py migrate

echo creating a superuser.
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(pk=1).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'ChangeMe!')"
python3 manage.py shell -c "from profiles.models import UserProfile; up=UserProfile.objects.get(pk=1); up.user_type='superadmin'; up.user_verified=1; up.save()"

echo creating staticinfo
python3 manage.py shell -c "from pages.models import StaticInfo; StaticInfo.objects.get_or_create(pk=1);"

echo Collecting static files
python3 manage.py collectstatic --noinput

echo Starting Gunicorn.
gunicorn olly._wsgi:application \
    --bind unix:/sock/olly.sock \
    --workers 2