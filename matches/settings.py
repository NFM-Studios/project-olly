from django.conf import settings

GAME_CHOICES = getattr(settings, 'MATCHES_GAMES_CHOICES', (
    (0, 'No Game Set'),
    (1, 'Call of Duty Black Ops 3'),
    (2, 'Call of Duty WWII'),
    (3, 'Fortnite'),
    (4, 'Destiny 2'),
    (5, 'Counter-Strike: Global Offensive'),
    (6, 'Player Unknowns Battlegrounds'),
    (7, 'Rainbow Six Siege'),
    (8, 'Overwatch'),
    (9, 'League of Legends'),
    (10, 'Hearthstone'),
    (11, 'World of Warcraft'),
    (12, 'Smite'),
    (13, 'Rocket League'),
    (14, 'Battlefield 1'),

))

PLATFORMS_CHOICES = getattr(settings, 'MATCHES_PLATFORMS_CHOICES', (
    (0, 'Playstation 4'),
    (1, 'Xbox One'),
    (2, 'PC'),
    (3, 'Mobile'),
    (4, 'Nintendo Switch'),
    (5, 'Playstation 3'),
    (6, 'Xbox 360'),
))

TEAMFORMAT_CHOICES = getattr(settings, 'MATCHES_TEAMFORMAT_CHOICES', (
    (0, '1v1'),
    (1, '2v2'),
    (2, '3v3'),
    (3, '4v4'),
    (4, '5v5'),
    (5, '6v6'),
))

MAPFORMAT_CHOICES = getattr(settings, 'MATCHES_MAPFORMAT_CHOICES', (
    (0, 'Best of 1'),
    (1, 'Best of 3'),
    (2, 'Best of 5'),
    (3, 'Best of 7'),
    (4, 'Best of 9'),
))