from django import forms
from .models import Client, MailingList


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['clients', 'send_time', 'frequency', 'status']
        widgets = {
            'clients': forms.CheckboxSelectMultiple(),
        }
