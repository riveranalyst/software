import django_filters

from .models import *


class TableFilter(django_filters.FilterSet):
    class Meta:
        model = Freezecore
        fields = [
                    'sample_id',
                    'sample_name',
                    'site_name',
                    'meas_station',
                    'meas_station__river',
                  ]
