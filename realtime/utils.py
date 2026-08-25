import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from profiles.models import Notification, UserProfile

logger = logging.getLogger(__name__)


def _resolve_user(user_or_profile):
    """Normalize a User or UserProfile to a User instance."""
    if isinstance(user_or_profile, User):
        return user_or_profile
    if isinstance(user_or_profile, UserProfile):
        return user_or_profile.user
    return user_or_profile


def _profile_for_user(user):
    """Return the UserProfile for a user, or None if it does not exist."""
    try:
        return UserProfile.objects.get(user=user)
    except (UserProfile.DoesNotExist, UserProfile.MultipleObjectsReturned):
        return None


def _publish_notification(user, notification):
    """Push a notification payload to the user's channel-layer group.

    Never raises: a channel-layer failure must not break the caller.
    """
    try:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return
        payload = {
            'action': 'notification',
            'id': notification.pk,
            'title': notification.title,
            'description': notification.description,
            'type': notification.type,
            'link': notification.link,
            'datetime': notification.datetime.isoformat(),
        }
        async_to_sync(channel_layer.group_send)(
            'user_%s' % user.pk,
            {'type': 'notification.message', 'message': payload},
        )
    except Exception:
        logger.exception('Failed to publish notification to channel layer for user %s', user.pk)


def notify_user(user, title, description='No description given', sender='System',
                type='general', link='', pk1=0, **extra):
    """Create a Notification for a user and push it over the channel layer.

    ``user`` may be a User or a UserProfile. If the user has no UserProfile
    the notification is still created and returned, but it is not attached
    to any profile and the channel-layer push is skipped.
    """
    user = _resolve_user(user)
    notification = Notification.objects.create(
        title=title,
        description=description,
        sender=sender,
        type=type,
        link=link,
        pk1=pk1,
        **extra
    )
    profile = _profile_for_user(user)
    if profile is None:
        logger.warning('No UserProfile for user %s; notification %s created but not attached',
                       user.pk, notification.pk)
    else:
        profile.notifications.add(notification)
    _publish_notification(user, notification)
    return notification


def notify_many(users, title, description='No description given', sender='System',
                type='general', link='', pk1=0, **extra):
    """Create the same Notification for each user in ``users``.

    ``users`` may be any iterable of User/UserProfile objects. Returns the
    list of created Notification instances (one per user).
    """
    notifications = []
    for user in users:
        notifications.append(
            notify_user(user, title=title, description=description, sender=sender,
                        type=type, link=link, pk1=pk1, **extra)
        )
    return notifications