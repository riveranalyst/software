from django import forms
from .models import SubsurfaceSed


class FreezecoreForm(forms.ModelForm):
    class Meta:
        model = SubsurfaceSed
        fields = '__all__'

