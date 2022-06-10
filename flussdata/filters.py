import django_filters

from .models import *


class TableFilter(django_filters.FilterSet):
    class Meta:
        model = Freezecore
        fields = ['river',
                  'sample_id',
                  'sample_name',
                  'site_name',
                  'date',
                  'time_stamp']
