import django_filters

from .models import *


class FreezecoreFilter(django_filters.FilterSet):
    class Meta:
        model = Freezecore
        fields = {
                    'sample_id': ['contains'],
                    # 'sample_name': ['contains'],
                    # 'site_name': ['contains'],
                    'meas_station': ['exact'],
        }


class IDOCFilter(FreezecoreFilter):
    class Meta:
        model = IDOC
        fields = {
                    'sample_id': ['contains'],
                    # 'sample_name': ['contains'],
                    # 'site_name': ['contains'],
                    'meas_station': ['exact'],
                    'meas_station__river': ['exact'],
                    'meas_station__campaign': ['exact'],
        }


class StationFilter(django_filters.FilterSet):
    class Meta:
        model = MeasStation
        fields = {'name': ['contains'],
                  'river': ['exact'],
                  'campaign': ['exact']}
