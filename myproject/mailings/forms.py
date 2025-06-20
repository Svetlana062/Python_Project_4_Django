from django import forms
from .models import Mailing, Message

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'status', 'message', 'recipients']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'messages': forms.Select(attrs={'class': 'form-control'}),
            'recipient': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
