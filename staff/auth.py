from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.shortcuts import render

from profiles.models import UserProfile

# 'admin' and 'superadmin' share identical permissions today (Phase 7 decision).
STAFF_TYPES = ('admin', 'superadmin')


def is_staff_user(user):
    """Return True if ``user`` is a logged-in user with a staff UserProfile."""
    if not user or user.is_anonymous:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return False
    return profile.user_type in STAFF_TYPES


def staff_required(view_func=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """Require an authenticated staff user.

    Anonymous users are redirected to the login page; authenticated non-staff
    users (or users without a UserProfile) get a 403 rendering
    'staff/permissiondenied.html'.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), login_url, redirect_field_name)
            if not is_staff_user(request.user):
                return HttpResponseForbidden(render(request, 'staff/permissiondenied.html'))
            return view(request, *args, **kwargs)
        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator


class StaffRequiredMixin:
    """Mixin for class-based staff views. Same behaviour as staff_required."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not is_staff_user(request.user):
            return HttpResponseForbidden(render(request, 'staff/permissiondenied.html'))
        return super().dispatch(request, *args, **kwargs)