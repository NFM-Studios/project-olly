from django import forms

from support.models import Ticket, TicketComment

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('subject', 'text')

class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('comment',)