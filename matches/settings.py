from django.conf import settings
from django.db import models


class TeamFormatChoices(models.IntegerChoices):
    ONE_V_ONE = 0, '1v1'
    TWO_V_TWO = 1, '2v2'
    THREE_V_THREE = 2, '3v3'
    FOUR_V_FOUR = 3, '4v4'
    FIVE_V_FIVE = 4, '5v5'
    SIX_V_SIX = 5, '6v6'


class MapFormatChoices(models.IntegerChoices):
    BEST_OF_1 = 1, 'Best of 1'
    BEST_OF_2 = 2, 'Best of 2'
    BEST_OF_3 = 3, 'Best of 3'
    BEST_OF_4 = 4, 'Best of 4'
    BEST_OF_5 = 5, 'Best of 5'


TEAMFORMAT_CHOICES = getattr(settings, 'MATCHES_TEAMFORMAT_CHOICES', TeamFormatChoices.choices)

MAPFORMAT_CHOICES = getattr(settings, 'MATCHES_MAPFORMAT_CHOICES', MapFormatChoices.choices)
