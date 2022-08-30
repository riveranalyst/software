import django_filters

from .models import *


class SubSurfFilter(django_filters.FilterSet):
    class Meta:
        model = SubsurfaceSed
        fields = {
                    'sample_id': ['contains'],
                    # 'sample_name': ['contains'],
                    # 'site_name': ['contains'],
                    'meas_station': ['exact'],
        }


class IDOCFilter(SubSurfFilter):
    class Meta:
        model = IDO
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
                  'campaign': ['exact'],
                  # 'collected_data': ['exact'],
                  'discharge': ['gte']}
