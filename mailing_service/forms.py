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
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = MailingList
        fields = ['clients', 'send_time', 'frequency', 'status', 'subject', 'body']
        widgets = {
            'send_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
