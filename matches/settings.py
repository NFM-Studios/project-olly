from django.conf import settings

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
