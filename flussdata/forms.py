from django import forms
from .models import SubsurfaceSed, CollectedData


class SubsurfaceForm(forms.ModelForm):
    class Meta:
        model = SubsurfaceSed
        fields = '__all__'


class DataForm(forms.ModelForm):
    class Meta:
        model = CollectedData
        fields = ['collected_data']
        # widget = forms.Select(attrs={"onChange": 'refresh()'})
        # queryset = CollectedData.objects.all().order_by('collected_data')


