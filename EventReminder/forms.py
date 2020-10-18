from django import forms
from .models import User, EventReminder

class CreateEvent(forms.ModelForm):
    class Meta:
        model = EventReminder
        fields = [
            'recipientMail',
            'messageDetail',
            'triggerDateTime'
        ]