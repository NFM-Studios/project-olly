from django.conf import settings
from django.db import models

# List of available status options


class TicketStatusChoices(models.IntegerChoices):
    NEW = 0, 'New'
    ON_HOLD = 1, 'On Hold'
    IN_PROGRESS = 2, 'In Progress'
    CLOSED = 3, 'Closed'


STATUS_CHOICES = getattr(settings, 'TICKETS_STATUS_CHOICES', TicketStatusChoices.choices)

# List of the different status that define a ticket as closed.
CLOSED_STATUSES = getattr(settings, 'TICKETS_CLOSED_STATUSES', (TicketStatusChoices.CLOSED, 4))
