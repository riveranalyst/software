import django_tables2 as tables
from flussdata.models import Freezecore


class FreezecoreTable(tables.Table):
    class Meta:
        model = Freezecore
        template_name = "django_tables2/bootstrap-responsive.html"
