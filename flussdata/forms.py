from django import forms
from .models import SubsurfaceSed, CollectedData


class SubsurfaceForm(forms.ModelForm):
    class Meta:
        model = SubsurfaceSed
        fields = '__all__'


class DataForm(forms.ModelForm):
    class Meta:
        model = CollectedData
        fields = '__all__'

