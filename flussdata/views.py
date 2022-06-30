from django.shortcuts import render
import flussdata.tables as flutb
from .filters import *
from .forms import *
from .alter_tables import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from django_pandas.io import read_frame
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .fill_fc_tab import *


def home(request):
    amount_fc = Freezecore.objects.count()
    context = {'amount_fc': amount_fc, 'navbar': 'home'}
    return render(request, 'home.html', context)


def query(request):
    #  Get all measurement data from the table
    freezecore_objects = Freezecore.objects.all()
    idoc_objects = IDOC.objects.all()
    station_objects = MeasStation.objects.all()

    # Get filter if the user selected any from the listed in filters.py
    fcFilter = FreezecoreFilter(request.GET, queryset=freezecore_objects)
    stFilter = StationFilter(request.GET, queryset=station_objects)

    # Apply filter, remaking the object
    freezecore_objects = fcFilter.qs
    station_objects = stFilter.qs
    freezecore_objects = freezecore_objects.filter(meas_station__name__in=station_objects.values('name'))
    idoc_objects = idoc_objects.filter(meas_station__name__in=station_objects.values('name'))

    # creates df from filtered table
    df_fc = read_frame(freezecore_objects)
    # df_idoc = read_frame(idoc_objects)
    df_stations = read_frame(station_objects)

    # Shows the table from the flussdata tables, hosted on tables.py
    table_show = flutb.FreezecoreTable(freezecore_objects)
    idoc_show = flutb.IDOCTable(idoc_objects).paginate(per_page=25)
    station_show = flutb.StationTable(station_objects).paginate(per_page=25)

    # table_show.paginate(page=request.GET.get("page", 1), per_page=25)

    # Count the amout of samples alter filte ris applied
    fc_count = freezecore_objects.count()
    idoc_count = idoc_objects.values_list('sample_id').distinct().count()

    # creates fig for mapbox using the df created from the filtered table
    fig = px.scatter_mapbox(df_stations,
                            lat='lat',
                            lon='lon',
                            # hover_name='sample_id',
                            color='name',
                            zoom=10,
                            # size='d50',
                            )

    fig.update_layout(
        mapbox_style="open-street-map",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # mapbox div
    mapboxdiv = plot(fig, output_type='div')

    # export of sub. sed. table
    RequestConfig(request).configure(table_show)
    export_format = request.GET.get("_export", None)

    RequestConfig(request).configure(station_show)
    export_format_st = request.GET.get("_export_st", None)

    RequestConfig(request).configure(idoc_show)
    export_format_idoc = request.GET.get("_export_idoc", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table_show)
        return exporter.response("freezecore-samples.{}".format(export_format))

    if TableExport.is_valid_format(export_format_st):
        exporter = TableExport(export_format_st, station_show)
        return exporter.response("stations.{}".format(export_format_st))

    if TableExport.is_valid_format(export_format_idoc):
        exporter = TableExport(export_format_idoc, idoc_show)
        return exporter.response("idoc.{}".format(export_format_idoc))

    #  return this to the context
    context = {'fcFilter': fcFilter,
               'stFilter': stFilter,
               # 'idocFilter': idocFilter,
               'table_show': table_show,
               'title': 'Flussdata: Query',
               'navbar': 'activequery',
               'fc_count': fc_count,
               'idoc_count': idoc_count,
               'idoc_table': idoc_show,
               'station_table': station_show,
               'mapboxfig': mapboxdiv}

    return render(request, 'flussdata/query.html', context)


# @require_http_methods(["GET"])
def view_sample(request, id):
    #  Get all measurement data from the table
    sample = get_object_or_404(Freezecore, id=id)
    print(sample)
    ds = ['250', '125', '63', '31_5', '16', '8', '4', '2', '1', '0_5', '0_25', '0_125', '0_063', '0_031']
    ds_float = [250, 125, 63, 31.5, 16, 4, 2, 1, 0.5, 0.25, 0.125, 0.063, 0.031]
    ds_values = []

    # loop through the sediment fractions, which are column names in the db
    for d in ds:
        ds_values.append(eval('sample.percent_finer_{0}mm'.format(d)))

    # graph embbeded ina  div to return to the template:
    fig = go.Figure()

    # create graph
    fig.add_trace(go.Scatter(x=ds_float, y=ds_values,
                             mode='lines', name='test',
                             opacity=0.8,
                             ))
    fig.update_xaxes(type="log")
    fig.update_layout(
        title='Grain Size Distribution ({0})'.format(sample.sample_id),
        xaxis_title='Grain size [mm]',
        yaxis_title='Percent finer [%]',
        height=420,
        width=560)

    # return graph div
    plot_div = plot(fig,
                    output_type='div')

    context = {'plot_div': plot_div}
    return render(request, 'flussdata/fc_sample.html', context)


def station_data(request, station_id):
    #  Get all measurement data from the table
    station = MeasStation.objects.get(id=station_id)
    fcs = Freezecore.objects.filter(meas_station=station_id)

    # graph embbeded ina  div to return to the template:
    fig = go.Figure()
    fig.update_layout(
        title='Grain Size Distribution',
        xaxis_title='Grain size [mm]',
        yaxis_title='Percent finer [%]',
        height=420,
        width=560)

    for fc in fcs:
        ds = ['250', '125', '63', '31_5', '16', '8', '4', '2', '1', '0_5', '0_25', '0_125', '0_063', '0_031']
        ds_float = [250, 125, 63, 31.5, 16, 4, 2, 1, 0.5, 0.25, 0.125, 0.063, 0.031]
        ds_values = []

        # loop through the sediment fractions, which are column names in the db
        for d in ds:
            ds_values.append(eval('fc.percent_finer_{0}mm'.format(d)))

        # create graph
        fig.add_trace(go.Scatter(x=ds_float, y=ds_values,
                                 mode='lines', name='test',
                                 opacity=0.8,
                                 hovertext=fc.sample_id,
                                 ))

    fig.update_xaxes(type="log")
    # return graph div
    plot_div = plot(fig, output_type='div')

    idocs = IDOC.objects.filter(meas_station_id=station_id)
    fig_idoc = go.Figure()
    fig_idoc.update_layout(
        #title='Intragravel Dissolved Oxygen Content',
        xaxis_title='Dissolved oxygen concentration [mg/L]',
        yaxis_title='Riverbed depth [m]',
        height=560,
        width=420)
    idoc_df = read_frame(idocs)
    for idoc in idoc_df['sample_id'].unique():
        idoc_sample = idoc_df[idoc_df['sample_id'] == idoc]
        fig_idoc.add_trace(go.Scatter(x=idoc_sample['idoc_mgl'],
                                      y=idoc_sample['sediment_depth_m'],
                                      mode='lines',
                                      hovertext=idoc_sample['sample_id'],
                                      ))
    fig_idoc.update_layout(yaxis=dict(showline=True,
                                      ticks='outside',
                                      range=[0.55, 0],
                                      tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5]
                                      ),
                           xaxis=dict(showline=True,
                                      ticks='outside',
                                      range=[0, 12],
                                      tickvals=[0, 2, 4, 6, 8, 10, 12],
                                      side='top'
                                      ))

    idoc_div = plot(fig_idoc, output_type='div')
    context = {'plot_div': plot_div, 'idoc_div': idoc_div, 'station_name': station.name}
    return render(request, 'flussdata/station_data.html', context)


class modifyView(TemplateView):
    template_name = 'flussdata/modify.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Flussdata: Modify'
        context['navbar'] = 'activemodify'
        return context

    def post(self, request):
        my_file = request.FILES['file']
        df = pd.read_csv(my_file.temporary_file_path(), encoding='utf-8', parse_dates=['date'])

        #  append data from df read into the database
        fill_fc_model(df)
        return JsonResponse({'post': 'false'})
