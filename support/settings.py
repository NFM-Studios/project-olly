from django.conf import settings

# List of available status options

STATUS_CHOICES = getattr(settings, 'TICKETS_STATUS_CHOICES', (
    (0, 'New'),
    (1, 'On Hold'),
    (2, 'In Progress'),
    (3, 'Closed'),
))

CATEGORY_CHOICES = getattr(settings, 'TICKETS_CATEGORY_CHOICES', (
    (0, 'General'),
    (1, 'Prize Claim'),
    (2, 'Tournament Support'),
    (3, 'Billing'),
    (4, 'Refund Request'),
    (5, 'PSN/XBL Issues'),
    (6, 'Match Support/Dispute'),
))

# List of the different status that define a ticket as closed.
CLOSED_STATUSES = getattr(settings, 'TICKETS_CLOSED_STATUSES', (3, 4))
