import django_filters

from .models import *


class SubSurfFilter(django_filters.FilterSet):
    class Meta:
        model = SubsurfaceSed
        fields = {
                    'sample_id': ['contains'],
                    # 'sample_name': ['contains'],
                    # 'site_name': ['contains'],
                    'meas_position': ['exact'],
        }


class IDOCFilter(SubSurfFilter):
    class Meta:
        model = IDO
        fields = {
                    'sample_id': ['contains'],
                    # 'sample_name': ['contains'],
                    # 'site_name': ['contains'],
                    'meas_position': ['exact'],
                    'meas_position__river': ['exact'],
                    'meas_position__survey': ['exact'],
        }


class PositionFilter(django_filters.FilterSet):
    class Meta:
        model = MeasPosition
        fields = {'name': ['contains'],
                  'river': ['exact'],
                  'survey': ['exact'],
                  # 'collected_data': ['exact'],
                  'discharge': ['gte']}
