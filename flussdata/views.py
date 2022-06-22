from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata
from flussdata.models import Freezecore
import flussdata.tables as flutb
from .filters import TableFilter
from .forms import *
from alter_tables import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from django_pandas.io import read_frame


def home(request):
    amount_fc = Freezecore.objects.count()
    context = {'amount_fc': amount_fc, 'navbar': 'home'}
    return render(request, 'home.html', context)


def query(request):
    #  Get all measurement data from the table
    freezecore_objects = Freezecore.objects.all()

    # Get filter if the user selected any from the listed in filters.py
    fcFilter = TableFilter(request.GET, queryset=freezecore_objects)

    # Apply filter, remaking the object
    freezecore_objects = fcFilter.qs

    # creates df from filtered table
    df = read_frame(freezecore_objects)

    # Shows the table from the flussdata tables, hosted on tables.py
    table_show = flutb.FreezecoreTable(freezecore_objects)

    # Count the amout of samples alter filte ris applied
    fc_count = freezecore_objects.count()

    fig = px.scatter_mapbox(df,
                            lat='lat',
                            lon='lon',
                            hover_name='sample_id',
                            color='river',
                            zoom=10)
    fig.update_layout(
        mapbox_style="open-street-map",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # mapbox div
    mapboxdiv = plot(fig,
                    output_type='div')

    #  return this to the context
    context = {'fcFilter': fcFilter, 'table_show': table_show,
               'title': 'Flussdata: Query', 'navbar': 'activequery',
               'fc_count': fc_count, 'mapboxfig': mapboxdiv}

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
        title='Grain Size Distribution ({0}/{1})'.format(sample.sample_id, sample.river),
        xaxis_title='Grain size [mm]',
        yaxis_title='Percent finer [%]',
        height=420,
        width=560)

    # return graph div
    plot_div = plot(fig,
                    output_type='div')

    context = {'plot_div': plot_div}
    return render(request, 'flussdata/fc_sample.html', context)


# def table(request):
#     form = FreezecoreForm()
#     context = {'form': form}
#     return render(request, 'flussdata/table.html', context)


def modify(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print('came here')
        try:
            append_freezecore(uploaded_file_url)
            message = "Successfully updated database table"
        except:
            message = "Something went wrong while updating database table, " \
                      "check your columns names."
    else:
        message = "sOmething wron"
    context = {'message': message, 'title': 'Flussdata: Modify', 'navbar': 'activemodify'}
    return render(request, 'flussdata/modify.html', context)


# def table(request):
#
#
#     return render(
#         request,
#         'flussdata/query.html', context)


