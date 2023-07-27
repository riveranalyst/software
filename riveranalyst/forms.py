from django import forms
from .models import SubsurfaceSed, CollectedData


class SubsurfaceForm(forms.ModelForm):
    class Meta:
        model = SubsurfaceSed
        fields = '__all__'


CHOICES = (('MeasPosition', 'Measurement positions Information'),
           ('IDO', 'Intragravel Dissolved Oxygen'),
           ('Kf', 'Hydraulic Conductivity'),
           ('SurfSed', 'Surface Sediment Sampling'),
           ('SubsurfSed', 'Subsurface Sediment Sampling'),
           ('Hydraulics', 'FlowTracker')
           )


class FileForm(forms.Form):
    collected_data = forms.MultipleChoiceField(choices=CHOICES)
