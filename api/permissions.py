from rest_framework.permissions import BasePermission, SAFE_METHODS

from staff.views import is_staff_user


class IsStaffOrReadOnly(BasePermission):
    """Allow read access to everyone; write access to staff users only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_staff_user(request.user)


class IsMatchParticipantOrStaff(BasePermission):
    """Allow write access to a match for staff users or the founder/captain
    of one of the two participating teams."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if is_staff_user(request.user):
            return True
        if not request.user or request.user.is_anonymous:
            return False
        for team in (obj.hometeam, obj.awayteam):
            if team is None:
                continue
            if team.founder_id == request.user.id:
                return True
            if team.captain.filter(id=request.user.id).exists():
                return True
        return False


class IsTeamOwnerOrStaff(BasePermission):
    """Allow write access to a team for staff users or the team's
    founder/captain."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if is_staff_user(request.user):
            return True
        if not request.user or request.user.is_anonymous:
            return False
        if obj.founder_id == request.user.id:
            return True
        return obj.captain.filter(id=request.user.id).exists()