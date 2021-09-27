from .models import *
from django import forms

class SmsConsumerForm(forms.ModelForm):
    class Meta:
        model = SmsLogModel
        fields = ['count']