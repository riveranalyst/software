import django_filters

from .models import *


class TableFilter(django_filters.FilterSet):
    class Meta:
        model = Freezecore
        fields = {
                    'sample_id': ['contains'],
                    'sample_name': ['contains'],
                    'site_name': ['contains'],
                    'meas_station': ['exact'],
                    'meas_station__river': ['exact'],
                    'meas_station__campaign': ['exact'],
        }
