from django import forms
from support.models import Ticket, TicketComment


class ListFilterForm(forms.Form):
    showClosed = forms.BooleanField(required=False, label='Show closed')
    searchQuery = forms.CharField(required=False, label='Search')


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ( 'category', 'text', )

    def __init__(self, *args, **kwargs):
        super(TicketCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'name': 'subject', 'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'name': 'texts', 'rows': '4', 'cols': '40'})


class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super(TicketCommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'name': 'comment', 'rows': '4', 'cols': '40'})


class TicketStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super(TicketStatusChangeForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'name': 'status', 'class': 'form-control'})
