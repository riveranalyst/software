from django import forms
from .models import Freezecore


class FreezecoreForm(forms.ModelForm):
    class Meta:
        model = Freezecore
        fields = '__all__'

