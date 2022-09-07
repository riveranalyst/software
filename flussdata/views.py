from django.shortcuts import render
import flussdata.tables as flutb
from .filters import *
from .forms import *
from plotly.offline import plot
import plotly.express as px
from django_pandas.io import read_frame
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from flussdata.utils.tables_append import append_db
from flussdata.utils.plotter import plot_gsd, plot_ido, plot_map, plot_kf
from django.contrib.auth.decorators import login_required, permission_required
import pandas as pd


def home(request):
    total_subsurf = SubsurfaceSed.objects.count()
    total_surf = SurfaceSed.objects.count()
    total_idoc = IDO.objects.values_list('sample_id').distinct().count()
    total_kf = Kf.objects.values_list('sample_id').distinct().count()
    total_v = Hydraulics.objects.count()

    context = {'navbar': 'home',
               'total_subsurf': total_subsurf,
               'total_surf': total_surf,
               'total_idoc': total_idoc,
               'total_kf': total_kf,
               'total_v': total_v}
    return render(request, 'home.html', context)


@login_required
@permission_required('flussdata.view_collecteddata', raise_exception=True)
def query(request):
    #  Get all measurement data from the table
    subsurf_objects = SubsurfaceSed.objects.all()
    surf_objects = SurfaceSed.objects.all()
    idoc_objects = IDO.objects.all()
    station_objects = MeasStation.objects.all()
    kf_objects = Kf.objects.all()
    v_objects = Hydraulics.objects.all()

    # Get filter if the user selected any from the listed in filters.py
    # subSurfFilter = SubSurfFilter(request.GET, queryset=subsurf_objects)
    stFilter = StationFilter(request.GET, queryset=station_objects)

    # Apply filter, remaking the object
    # subsurf_objects = subSurfFilter.qs
    station_objects = stFilter.qs
    subsurf_objects = subsurf_objects.filter(meas_station__name__in=station_objects.values('name'))

    idoc_objects = idoc_objects.filter(meas_station__name__in=station_objects.values('name'))
    surf_objects = surf_objects.filter(meas_station__name__in=station_objects.values('name'))
    kf_objects = kf_objects.filter(meas_station__name__in=station_objects.values('name'))
    v_objects = v_objects.filter(meas_station__name__in=station_objects.values('name'))

    # creates df from filtered table
    df_stations = read_frame(station_objects)

    # Shows the table from the flussdata tables, hosted on tables.py
    subsurf_tb_show = flutb.SubsurfaceTable(subsurf_objects).paginate(per_page=10)
    surf_tb_show = flutb.SurfaceTable(surf_objects).paginate(per_page=10)
    idoc_show = flutb.IDOCTable(idoc_objects).paginate(per_page=10)
    station_show = flutb.StationTable(station_objects).paginate(per_page=10)
    kf_show = flutb.KfTable(kf_objects).paginate(per_page=10)

    # Count the number of samples alter filte ris applied
    subsurf_count = subsurf_objects.count()
    surf_count = surf_objects.count()
    kf_count = kf_objects.values_list('sample_id').distinct().count()
    v_count = v_objects.count()
    idoc_count = idoc_objects.values_list('sample_id').distinct().count()

    # create new columns with computed lat and log in the projection
    # accepted by the mapbox (epsg:4326)

    # creates fig for mapbox using the df created from the filtered table
    fig = plot_map(df_stations)

    # mapbox div
    mapboxdiv = plot(fig, output_type='div')

    # export of sub. sed. table
    RequestConfig(request).configure(subsurf_tb_show)
    export_format = request.GET.get("_export", None)

    RequestConfig(request).configure(surf_tb_show)
    export_format_surf = request.GET.get("_export_surf", None)

    RequestConfig(request).configure(station_show)
    export_format_st = request.GET.get("_export_st", None)

    RequestConfig(request).configure(idoc_show)
    export_format_idoc = request.GET.get("_export_idoc", None)

    RequestConfig(request).configure(kf_show)
    export_format_kf = request.GET.get("_export_kf", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, subsurf_tb_show)
        return exporter.response("subsurface-samples.{}".format(export_format))

    if TableExport.is_valid_format(export_format_surf):
        exporter = TableExport(export_format_idoc, idoc_show)
        return exporter.response("surface-samples.{}".format(export_format_idoc))

    if TableExport.is_valid_format(export_format_st):
        exporter = TableExport(export_format_st, station_show)
        return exporter.response("stations.{}".format(export_format_st))

    if TableExport.is_valid_format(export_format_idoc):
        exporter = TableExport(export_format_idoc, idoc_show)
        return exporter.response("idoc.{}".format(export_format_idoc))

    if TableExport.is_valid_format(export_format_kf):
        exporter = TableExport(export_format_kf, kf_show)
        return exporter.response("kf.{}".format(export_format_kf))

    #  return this to the context
    context = {'title': 'Flussdata: Query',  # pagetitle
               'navbar': 'activequery',  # make the tab 'query' highlighted

               # number of measurements for the selected query
               'subsurf_count': subsurf_count,
               'surf_count': surf_count,
               'idoc_count': idoc_count,
               'kf_count': kf_count,
               'v_count': v_count,

               # filters
               # 'subSurfFilter': subSurfFilter,
               'stFilter': stFilter,
               # 'idocFilter': idocFilter,

               # tables
               'subsurf_tb_show': subsurf_tb_show,
               'idoc_table': idoc_show,
               'station_table': station_show,
               'surf_tb_show': surf_tb_show,
               'kf_table': kf_show,

               # mapbox
               'mapboxfig': mapboxdiv}

    return render(request, 'flussdata/query.html', context)


@login_required
@permission_required('flussdata.view_collected_data', raise_exception=True)
def station_data(request, station_id):
    #  Get all measurement data from the table
    gsds = []
    station = MeasStation.objects.get(id=station_id)
    subsurf_sample = SubsurfaceSed.objects.filter(meas_station=station_id)
    surf_sample = SurfaceSed.objects.filter(meas_station=station_id)

    if surf_sample:
        fig_surf = plot_gsd(surf_sample, title='Surface Grain Size Distribution')
        # return graph div
        plot_div = plot(fig_surf, output_type='div')
        gsds.append(plot_div)

    if subsurf_sample:
        fig_subsurf = plot_gsd(subsurf_sample, title='Subsurface Grain Size Distribution')
        # return graph div
        plot_div = plot(fig_subsurf, output_type='div')
        gsds.append(plot_div)

    # generating fig for idocs
    idocs = IDO.objects.filter(meas_station_id=station_id)
    if idocs:
        fig_idoc = plot_ido(idocs)
        idoc_div = plot(fig_idoc, output_type='div')
    else:
        idoc_div = None

    # generating fig for kf
    kfs = Kf.objects.filter(meas_station_id=station_id)
    if kfs:
        fig_kf = plot_kf(kfs)
        kf_div = plot(fig_kf, output_type='div')
    else:
        kf_div = None
    context = {'gsds': gsds, 'idoc_div': idoc_div, 'kf_div': kf_div, 'station_name': station.name}
    return render(request, 'flussdata/station_data.html', context)


@login_required
@permission_required('flussdata.add_collected_data', raise_exception=True)
def modify(request):
    context = {'title': 'Flussdata: Modify',
               'form': FileForm,
               'navbar': 'activemodify'}
    return render(request, 'flussdata/modify.html', context)


@login_required
@permission_required('flussdata.add_collected_data', raise_exception=True)
def upload_file(request):
    global MESSAGE
    MESSAGE = 'Fail: Please select the collected data.'
    if request.method == 'POST':
        if request.POST['collected_data']:
            try:
                my_file = request.FILES['file']  # gets the table file from the post request
                df = pd.read_csv(my_file.temporary_file_path(), encoding='utf-8',
                                 parse_dates=['date'])

                #  append data from df read into the database
                append_db(request.POST['collected_data'], df)
                MESSAGE = 'Success: File was parsed and appended to the database.'
            except Exception as e:
                # TODO
                # send message to user to make him selecte a collected data
                # return render(request, 'flussdata/modify.html', {'message': 'Incorrect data'})
                MESSAGE = 'Fail: File could not be parsed and appended ' \
                          'to the database. Error messages: \n' + str(e)
    return JsonResponse({'post': 'false'})


@login_required
@permission_required('flussdata.add_collected_data', raise_exception=True)
def success_upload(request):
    return render(request, 'flussdata/success_upload.html', {'message': MESSAGE})


def dashboard(request):
    #  Get all measurement data from the table
    subsurf_objects = SubsurfaceSed.objects.all()
    surf_objects = SurfaceSed.objects.all()
    idoc_objects = IDO.objects.all()
    station_objects = MeasStation.objects.all()
    kf_objects = Kf.objects.all()
    v_objects = Hydraulics.objects.all()

    # Get filter if the user selected any from the listed in filters.py
    # subSurfFilter = SubSurfFilter(request.GET, queryset=subsurf_objects)
    stFilter = StationFilter(request.GET, queryset=station_objects)

    # Apply filter, remaking the object
    # subsurf_objects = subSurfFilter.qs
    station_objects = stFilter.qs
    subsurf_objects = subsurf_objects.filter(meas_station__name__in=station_objects.values('name'))

    idoc_objects = idoc_objects.filter(meas_station__name__in=station_objects.values('name'))
    surf_objects = surf_objects.filter(meas_station__name__in=station_objects.values('name'))
    kf_objects = kf_objects.filter(meas_station__name__in=station_objects.values('name'))
    v_objects = v_objects.filter(meas_station__name__in=station_objects.values('name'))

    # creates df from filtered table
    df_fc = read_frame(subsurf_objects)
    # df_idoc = read_frame(idoc_objects)
    df_stations = read_frame(station_objects)

    # Shows the table from the flussdata tables, hosted on tables.py
    subsurf_tb_show = flutb.SubsurfaceTable(subsurf_objects)
    idoc_show = flutb.IDOCTable(idoc_objects).paginate(per_page=25)
    station_show = flutb.StationTable(station_objects).paginate(per_page=25)

    # subsurf_tb_show.paginate(page=request.GET.get("page", 1), per_page=25)

    # Count the number of samples alter filte ris applied
    subsurf_count = subsurf_objects.count()
    surf_count = surf_objects.count()
    kf_count = kf_objects.count()
    v_count = v_objects.count()

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
        legend_title_text='Stations'
    )
    fig.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10})

    # mapbox div
    mapboxdiv = plot(fig, output_type='div')

    # export of sub. sed. table
    RequestConfig(request).configure(subsurf_tb_show)
    export_format = request.GET.get("_export", None)

    RequestConfig(request).configure(station_show)
    export_format_st = request.GET.get("_export_st", None)

    RequestConfig(request).configure(idoc_show)
    export_format_idoc = request.GET.get("_export_idoc", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, subsurf_tb_show)
        return exporter.response("subsurface-samples.{}".format(export_format))

    if TableExport.is_valid_format(export_format_st):
        exporter = TableExport(export_format_st, station_show)
        return exporter.response("stations.{}".format(export_format_st))

    if TableExport.is_valid_format(export_format_idoc):
        exporter = TableExport(export_format_idoc, idoc_show)
        return exporter.response("idoc.{}".format(export_format_idoc))

    #  return this to the context
    context = {'title': 'Flussdata: Dashboard',  # pagetitle
               'navbar': 'activedash',  # make the tab 'query' highlighted

               # number of measurements for the selected query
               'subsurf_count': subsurf_count,
               'surf_count': surf_count,
               'idoc_count': idoc_count,
               'kf_count': kf_count,
               'v_count': v_count,

               # filters
               # 'subSurfFilter': subSurfFilter,
               'stFilter': stFilter,
               # 'idocFilter': idocFilter,

               # tables
               'subsurf_tb_show': subsurf_tb_show,
               'idoc_table': idoc_show,
               'station_table': station_show,

               # mapbox
               'mapboxfig': mapboxdiv}

    return render(request, 'flussdata/dashboard.html', context)