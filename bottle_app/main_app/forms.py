from django import forms
from .models import *

class BottleForm(forms.ModelForm):
    class Meta:
        models = Bottle
        fields = ['text', 'range']
    