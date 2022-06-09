import django_tables2
from flussdata.models import Freezecore


class FreezecoreTable(django_tables2.Table):
    class Meta:
        model = Freezecore
