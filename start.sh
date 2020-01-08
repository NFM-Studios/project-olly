#!/bin/bash
echo Debug is $debug

echo Running Migrations.
python3 manage.py migrate

echo creating a superuser.
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(pk=1).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'ChangeMe!')"
python3 manage.py shell -c "from profiles.models import UserProfile; up=UserProfile.objects.get(pk=1); up.user_type='superadmin'; up.user_verified=1; up.save()"

echo creating staticinfo
python3 manage.py shell -c "from pages.models import StaticInfo; StaticInfo.objects.get_or_create(pk=1);"

echo creating default esports platforms
python3 manage.py shell -c "from matches.models import PlatformChoice; PlatformChoice.objects.get_or_create(name='Playstation 4')"
python3 manage.py shell -c "from matches.models import PlatformChoice; PlatformChoice.objects.get_or_create(name='Xbox One')"
python3 manage.py shell -c "from matches.models import PlatformChoice; PlatformChoice.objects.get_or_create(name='Mobile')"
python3 manage.py shell -c "from matches.models import PlatformChoice; PlatformChoice.objects.get_or_create(name='PC')"
python3 manage.py shell -c "from matches.models import PlatformChoice; PlatformChoice.objects.get_or_create(name='Nintendo Switch')"

echo creating default esports games
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Counter-Strike: Global Offensive')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='League of Legends')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Overwatch')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Rocket League')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Dota 2')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Hearthstone')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Fortnite')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='SMITE')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Rainbow Six Siege')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Heroes of the Storm')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Call of Duty: Modern Warfare')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Apex Legends')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Super Smash Bros. Ultimate')"
python3 manage.py shell -c "from matches.models import GameChoice; GameChoice.objects.get_or_create(name='Clash Royale')"

echo creating default sports choices
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Ice Hockey')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Soccer')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Indoor Soccer')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Futsal')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Roller Hockey')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Basketball')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Football')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Lacrosse')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Baseball')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Kan Jam')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Spikeball')"
python3 manage.py shell -c "from matches.models import SportChoice; SportChoice.objects.get_or_create(name='Ultimate')"

echo Collecting static files
python3 manage.py collectstatic --noinput

echo Starting Gunicorn.
gunicorn olly.wsgi:application \
    --bind unix:/sock/olly.sock \
    --workers 2
