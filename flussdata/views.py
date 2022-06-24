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


def home(request):
    amount_fc = Freezecore.objects.count()
    context = {'amount_fc': amount_fc, 'navbar': 'home'}
    return render(request, 'home.html', context)


def query(request):
    #  Get all measurement data from the table
    freezecore_objects = Freezecore.objects.all()
    idoc_objects = Freezecore.objects.all()

    # Get filter if the user selected any from the listed in filters.py
    # TODO modify or somehow adapt code below to instantiate a sort of
    #  MeasPoint filter objects and use it for filtering both models
    fcFilter = FreezecoreFilter(request.GET, queryset=freezecore_objects)

    # Apply filter, remaking the object
    freezecore_objects = fcFilter.qs
    # idoc_objects =


    # creates df from filtered table
    df = read_frame(freezecore_objects)

    # Shows the table from the flussdata tables, hosted on tables.py
    table_show = flutb.FreezecoreTable(freezecore_objects)
    idoc_show = flutb.IDOCTable(idoc_objects)

    # table_show.paginate(page=request.GET.get("page", 1), per_page=25)

    # Count the amout of samples alter filte ris applied
    fc_count = freezecore_objects.count()
    # idoc_count =

    # creates fig for mapbox using the df created from the filtered table
    fig = px.scatter_mapbox(df,
                            lat='lat',
                            lon='lon',
                            hover_name='sample_id',
                            color='meas_station',
                            zoom=10,
                            size='d50', )
    fig.update_layout(
        mapbox_style="open-street-map",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # mapbox div
    mapboxdiv = plot(fig, output_type='div')

    # export of sub. sed. table
    RequestConfig(request).configure(table_show)
    export_format = request.GET.get("_export", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table_show)
        return exporter.response("table.{}".format(export_format))

    #  return this to the context
    context = {'fcFilter': fcFilter, 'table_show': table_show,
               'title': 'Flussdata: Query', 'navbar': 'activequery',
               'fc_count': fc_count,
               # 'idoc_count': idoc_count,
               'idoc_table': idoc_show,
               'mapboxfig': mapboxdiv}

    return render(request, 'flussdata/query.html', context)


@require_http_methods(["GET"])
def view_sample(request, id):
    #  Get all measurement data from the table
    sample = get_object_or_404(Freezecore, id=id)
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


class modifyView(TemplateView):
    template_name = 'flussdata/modify.html'


def file_upload_view(request):
    # print(request.FILES)
    # return HttpResponse('modify/upload')
    # context = {}
    if request.method == 'POST':
        my_file = request.FILES['file']
    #     fs = FileSystemStorage()
    #     filename = fs.save(my_file.name, my_file)
    #     uploaded_file_url = fs.url(filename)
        df = pd.read_csv(my_file.temporary_file_path(), encoding='utf-8', parse_dates=['date'])
        print(my_file.temporary_file_path())
        #  append data from df read into the database
        for index, row in df.iterrows():
            obj = models.Freezecore.objects.create(
                river=row.river,
                sample_id=row.sample_id,
                sample_name=row.sample_name,
                site_name=row.site_name,
                date=row.date,
                time_stamp=row.time_stamp,
                lon=row.lon,
                lat=row.lat,
                porosity_sfm=row.porosity_sfm,
                dm=row.dm,
                dg=row.dg,
                fi=row.fi,
                geom_std_grain=row.geom_std_grain,
                d10=row.d10,
                d16=row.d16,
                d25=row.d25,
                d30=row.d30,
                d50=row.d50,
                d60=row.d60,
                d75=row.d75,
                d84=row.d84,
                d90=row.d90,
                cu=row.cu,
                cc=row.cc,
                fsf_le_2mm=row.fsf_le_2mm,
                fsf_le_1mm=row.fsf_le_1mm,
                fsf_le_0_5mm=row.fsf_le_0_5mm,
                so=row.so,
                wl_slurp_m=row.wl_slurp_m,
                wl_model_m=row.wl_model_m,
                n_wooster=row.n_wooster,
                bed_slope=row.bed_slope,
                comment=row.comment,
                percent_finer_250mm=row.percent_finer_250mm,
                percent_finer_125mm=row.percent_finer_125mm,
                percent_finer_63mm=row.percent_finer_63mm,
                percent_finer_31_5mm=row.percent_finer_31_5mm,
                percent_finer_16mm=row.percent_finer_16mm,
                percent_finer_8mm=row.percent_finer_8mm,
                percent_finer_4mm=row.percent_finer_4mm,
                percent_finer_2mm=row.percent_finer_2mm,
                percent_finer_1mm=row.percent_finer_1mm,
                percent_finer_0_5mm=row.percent_finer_0_5mm,
                percent_finer_0_25mm=row.percent_finer_0_25mm,
                percent_finer_0_125mm=row.percent_finer_0_125mm,
                percent_finer_0_063mm=row.percent_finer_0_063mm,
                percent_finer_0_031mm=row.percent_finer_0_031mm)
            obj.save()
        return HttpResponse('')
    return JsonResponse({'post': 'false'})


    # if request.method == 'POST' and request.FILES['myfile']:
    #     myfile = request.FILES['myfile']
    #     print(myfile)
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     print('came here')
    #     try:
    #         append_freezecore(uploaded_file_url)
    #         message = "Successfully updated database table"
    #     except:
    #         message = "Something went wrong while updating database table, " \
    #                   "check your columns names."
    # else:
    #     message = "sOmething wron"
    # context = {'message': message, 'title': 'Flussdata: Modify', 'navbar': 'activemodify'}
    # return render(request, 'flussdata/modify.html', context)