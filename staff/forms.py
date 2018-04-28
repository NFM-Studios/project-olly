from django import forms
from pages.models import StaticInfo
from profiles.models import UserProfile
from support.models import TicketComment
from matches.models import Match
from singletournaments.models import SingleEliminationTournament
from news.models import Post


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
        widgets = {
            'open_register': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'close_register': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'start': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }


class DeclareMatchWinnerForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('winner', 'completed', 'disputed')


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
