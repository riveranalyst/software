import django_tables2 as tables
from flussdata.models import *
from django.utils.html import format_html
from django.urls import reverse


class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.2f}'.format(value)


class ExponentColumn(tables.Column):
    def render(self, value):
        return '{:1.1e}'.format(value)


class SubsurfaceTable(tables.Table):
    n_user = NumberColumn()
    dm = NumberColumn()
    dg = NumberColumn()
    fi = NumberColumn()
    geom_std_grain = NumberColumn()
    d10 = NumberColumn()
    d16 = NumberColumn()
    d25 = NumberColumn()
    d30 = NumberColumn()
    d50 = NumberColumn()
    d60 = NumberColumn()
    d75 = NumberColumn()
    d84 = NumberColumn()
    d90 = NumberColumn()
    cu = NumberColumn()
    cc = NumberColumn()
    fsf_le_2mm = NumberColumn()
    fsf_le_1mm = NumberColumn()
    fsf_le_0_5mm = NumberColumn()
    so = NumberColumn()
    wl_slurp_m = NumberColumn()
    wl_model_m = NumberColumn()
    n_wooster = NumberColumn()
    bed_slope = NumberColumn()
    percent_finer_250mm = NumberColumn()
    percent_finer_125mm = NumberColumn()
    percent_finer_63mm = NumberColumn()
    percent_finer_31_5mm = NumberColumn()
    percent_finer_16mm = NumberColumn()
    percent_finer_8mm = NumberColumn()
    percent_finer_4mm = NumberColumn()
    percent_finer_2mm = NumberColumn()
    percent_finer_1mm = NumberColumn()
    percent_finer_0_5mm = NumberColumn()
    percent_finer_0_25mm = NumberColumn()
    percent_finer_0_125mm = NumberColumn()
    percent_finer_0_063mm = NumberColumn()
    percent_finer_0_031mm = NumberColumn()

    class Meta:
        model = SubsurfaceSed
        template_name = "django_tables2/bootstrap-responsive.html"

    # def render_sample_id(self, record):
    #     return format_html('<a href="{}"><button class="btn btn-primary" type="submit">{'
    #                        '}</button></a>', reverse('flussdata:view_sample', kwargs={'id': record.id}),
    #                        record.sample_id)


class SurfaceTable(tables.Table):
    dm = NumberColumn()
    dg = NumberColumn()
    fi = NumberColumn()
    geom_std_grain = NumberColumn()
    d10 = NumberColumn()
    d16 = NumberColumn()
    d25 = NumberColumn()
    d30 = NumberColumn()
    d50 = NumberColumn()
    d60 = NumberColumn()
    d75 = NumberColumn()
    d84 = NumberColumn()
    d90 = NumberColumn()
    cu = NumberColumn()
    cc = NumberColumn()
    fsf_le_2mm = NumberColumn()
    fsf_le_1mm = NumberColumn()
    fsf_le_0_5mm = NumberColumn()
    so = NumberColumn()
    wl_slurp_m = NumberColumn()
    wl_model_m = NumberColumn()
    n_wooster = NumberColumn()
    bed_slope = NumberColumn()
    percent_finer_250mm = NumberColumn()
    percent_finer_125mm = NumberColumn()
    percent_finer_63mm = NumberColumn()
    percent_finer_31_5mm = NumberColumn()
    percent_finer_16mm = NumberColumn()
    percent_finer_8mm = NumberColumn()
    percent_finer_4mm = NumberColumn()
    percent_finer_2mm = NumberColumn()
    percent_finer_1mm = NumberColumn()
    percent_finer_0_5mm = NumberColumn()
    percent_finer_0_25mm = NumberColumn()
    percent_finer_0_125mm = NumberColumn()
    percent_finer_0_063mm = NumberColumn()
    percent_finer_0_031mm = NumberColumn()

    class Meta:
        model = SurfaceSed
        template_name = "django_tables2/bootstrap-responsive.html"


class IDOCTable(tables.Table):
    sediment_depth_m = NumberColumn()
    idoc_mgl = NumberColumn()
    kf_ms = NumberColumn()

    class Meta:
        model = Kf


class KfTable(tables.Table):
    sediment_depth_m = NumberColumn()
    slurp_rate_avg_mls = NumberColumn()
    temp_c = NumberColumn()
    idoc_sat = NumberColumn()

    class Meta:
        model = IDO
        # template_name = "django_tables2/bootstrap-responsive.html"


class StationTable(tables.Table):
    wl_m = NumberColumn()
    H_m = NumberColumn()
    data = tables.Column(empty_values=())

    class Meta:
        model = MeasStation
        template_name = "django_tables2/bootstrap-responsive.html"
        sequence = ('id', 'name', 'data', '...')

    def render_data(self, record):
        return format_html('<a href="{}"><button class="btn btn-primary" type="submit">View'
                           '</button></a>',
                           reverse('flussdata:station_data', kwargs={'station_id': record.id}))
