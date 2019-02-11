from django import forms

from .models import Transfer


class TransferCreditsForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['credits', 'destination_user']

    destination_user = forms.CharField(required=True, max_length=50)
    credits = forms.DecimalField(required=True, decimal_places=0)
    confirm = forms.BooleanField(required=True)
