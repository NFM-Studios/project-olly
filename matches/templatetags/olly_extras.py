from datetime import date, datetime

from django import template
from django.template.defaultfilters import date as django_date
from django.utils.html import escapejs

register = template.Library()


@register.filter
def js_datetime(value):
    """Render a datetime as an ISO 8601 string that is safe inside a JS string literal."""
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return django_date(value, "c")
    return escapejs(value)


@register.filter
def js_string(value):
    """Escape a value for safe embedding inside a JS string literal."""
    if value is None:
        return ""
    return escapejs(value)


@register.filter
def teamformat(value):
    """Map numeric team formats (0-5) to display names like '1v1'."""
    formats = {0: '1v1', 1: '2v2', 2: '3v3', 3: '4v4', 4: '5v5', 5: '6v6'}
    try:
        return formats.get(int(value), 'Unknown')
    except (TypeError, ValueError):
        return 'Unknown'


@register.filter
def bestof(value):
    """Map numeric best-of values (1-5) to display names like 'Best of 3'."""
    formats = {1: 'Best of 1', 2: 'Best of 2', 3: 'Best of 3', 4: 'Best of 4', 5: 'Best of 5'}
    try:
        return formats.get(int(value), 'Unknown')
    except (TypeError, ValueError):
        return 'Unknown'