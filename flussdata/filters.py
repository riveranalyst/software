import django_filters

from .models import *


class TableFilter(django_filters.FilterSet):
    class Meta:
        model = Freezecore
        fields = {
                    'sample_id': ['exact', 'contains'],
                    'sample_name': ['exact', 'contains'],
                    'site_name': ['exact', 'contains'],
                    'meas_station': ['exact'],
                    'meas_station__river': ['exact'],
                    'meas_station__campaign': ['exact'],
        }
