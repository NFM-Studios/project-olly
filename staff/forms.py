from django import forms
from pages.models import StaticInfo, Partner
from profiles.models import UserProfile
from support.models import TicketComment
from matches.models import Match
from singletournaments.models import SingleEliminationTournament, SingleTournamentRuleset
from news.models import Post
from support.models import TicketComment, Ticket
from teams.models import Team, TeamInvite
from store.models import Product


class StaticInfoForm(forms.ModelForm):
    class Meta:
        model = StaticInfo
        fields = ('about_us', 'terms', 'stream', 'slide1link', 'slide1_img',
                  'slide2link', 'slide2_img', 'slide3link', 'slide3_img', 'welcomeln1',
                  'welcomeln2')

    def __init__(self, request, *args, **kwargs):
        if request.tenant == 'binge':
            newfields = ('bingetop1', 'bingetop2', 'bingetop3', 'bingetop1link', 'bingetop2link',
                         'bingetop3link', 'bingeslide1big', 'bingeslide2big', 'bingeslide3big',
                         'bingeslide1small', 'bingeslide2small', 'bingeslide3small', 'bingeslide1link',
                         'bingeslide1link', 'bingeslide2link', 'bingeslide3link')
        super().__init__(request, *args, **kwargs)
        self.fields = self.fields + newfields


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'


class SingleRulesetCreateForm(forms.ModelForm):
    class Meta:
        model = SingleTournamentRuleset
        fields = ('name', 'text')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type',)


class TicketSearchForm(forms.Form):
    showClosed = forms.BooleanField(required=False, label='Show closed')
    searchQuery = forms.CharField(required=False, label='Search')


class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('comment',)


class EditTournamentForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationTournament
        fields = '__all__'
        widgets = {
            'open_register': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1', 'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
            'close_register': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker2', 'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker2'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker3', 'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker3'})
        }


class DeclareMatchWinnerForm(forms.ModelForm):
    winner = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Match
        #fields = ('winner',)
        fields = ()

    def __init__(self, request, pk, *args, **kwargs):
        match = Match.objects.filter(id=pk)
        team1 = Team.objects.filter(id__in=match.values_list('hometeam', flat=True))
        team2 = Team.objects.filter(id__in=match.values_list('awayteam', flat=True))
        super().__init__(*args, **kwargs)
        self.fields['winner'].queryset = team1 | team2


class DeclareMatchWinnerPost(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('winner', 'completed')


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'slug', 'body', 'publish', 'status')
        widgets = {
            'publish': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),

        }


class TicketStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('status',)


class DeclareTournamentWinnerForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationTournament
        fields = ('winner', 'second', 'third')


class CreateNewsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class EditNewsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'publish': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
        }


class RemovePlayerForm(forms.ModelForm):
    remove = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = TeamInvite
        fields = ()

    def __init__(self, request, pk, *args, **kwargs):
        team = Team.objects.get(id=pk)
        players = TeamInvite.objects.filter(team=team, accepted=True)
        super().__init__(*args, **kwargs)
        self.fields['remove'].queryset = players


class RemovePlayerFormPost(forms.ModelForm):
    remove = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = TeamInvite
        fields = ()


class AddCreditsForm(forms.Form):
    credits = forms.IntegerField(required=True)

    class Meta:
        fields = 'credits'


class AddXPForm(forms.Form):
    xp = forms.IntegerField(required=True)

    class Meta:
        fields = "XP"


class AddTrophiesForm(forms.Form):
    bronze = forms.IntegerField(required=True)
    silver = forms.IntegerField(required=True)
    gold = forms.IntegerField(required=True)

    class Meta:
        fields = ('Bronze', 'Silver', 'Gold')


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('amount', 'item_name', 'price', 'name', 'active')


class EditProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('amount', 'item_name', 'price', 'name', 'active')


class DeleteProductForm(forms.Form):
    price = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)

    class Meta:
        fields = ('price', 'name')


class RemovePostForm(forms.Form):
    slug = forms.CharField(required=True, max_length=250)

