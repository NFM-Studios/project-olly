from django import forms
from pages.models import StaticInfo
from profiles.models import UserProfile
from support.models import TicketComment
from singletournaments.models import SingleEliminationTournament


class StaticInfoForm(forms.ModelForm):
    class Meta:
        model = StaticInfo
        fields = ('about_us', 'terms', 'privacy')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type',)


class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('comment',)


class EditTournamentForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationTournament
        fields = '__all__'
