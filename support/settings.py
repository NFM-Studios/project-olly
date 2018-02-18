from django.conf import settings

# List of available status options

STATUS_CHOICES = getattr(settings, 'TICKETS_STATUS_CHOICES', (
    (0, 'New'),
    (1, 'On Hold'),
    (2, 'In Progress'),
    (3, 'Resolved'),
    (4, 'Closed'),
))

# List of the different status that define a ticket as closed.
CLOSED_STATUSES = getattr(settings, 'TICKETS_CLOSED_STATUSES', (3, 4))
