#!/bin/bash
set -euo pipefail

echo "Debug is ${debug:-unset}"

echo "Waiting for the database and running migrations."
migrated=0
for i in $(seq 1 30); do
    if python3 manage.py migrate; then
        migrated=1
        break
    fi
    echo "Database not ready yet (attempt ${i}/30), retrying in 2s..."
    sleep 2
done

if [ "${migrated}" -ne 1 ]; then
    echo "Database never became ready. Aborting." >&2
    exit 1
fi

echo "Creating a superuser."
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(pk=1).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'ChangeMe!')"
python3 manage.py shell -c "from profiles.models import UserProfile; up=UserProfile.objects.get(pk=1); up.user_type='superadmin'; up.user_verified=1; up.save()"

echo "Creating staticinfo"
python3 manage.py shell -c "from pages.models import StaticInfo; StaticInfo.objects.get_or_create(pk=1);"

echo "Creating socialinfo"
python3 manage.py shell -c "from pages.models import SocialInfo; SocialInfo.objects.get_or_create(pk=1);"

echo "Collecting static files"
python3 manage.py collectstatic --noinput

echo "Starting Gunicorn."
exec gunicorn olly.wsgi:application \
    --bind unix:/sock/olly.sock \
    --bind 127.0.0.1:8000 \
    --workers "${WEB_CONCURRENCY:-3}"