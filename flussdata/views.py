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


def home(request):
    amount_fc = Freezecore.objects.count()
    context = {'amount_fc': amount_fc, 'navbar': 'home'}
    return render(request, 'home.html', context)


def query(request):
    #  Get all measurement data from the table
    freezecore_objects = Freezecore.objects.all()

    # Get filter if the user selected any
    myFilter = TableFilter(request.GET, queryset=freezecore_objects)

    # Apply filter, remaking the object
    freezecore_objects = myFilter.qs

    # Shows the table from the flussdata tables, hosted on tables.py
    table_show = flutb.FreezecoreTable(freezecore_objects)

    #  return this to the context
    context = {'myFilter': myFilter, 'table_show': table_show,
               'title': 'Flussdata: Query', 'navbar': 'activequery'}

    return render(request, 'flussdata/query.html', context)


@require_http_methods(["GET"])
def view_sample(request, id):
    #  Get all measurement data from the table
    sample = get_object_or_404(Freezecore, id=id)
    ds = ['250', '125', '63', '31_5', '16', '8', '4', '2', '1', '0_5', '0_25', '0_125', '0_063', '0_031']
    ds_float = [250, 125, 63, 31.5, 16, 4, 2, 1, 0.5, 0.25, 0.125, 0.063, 0.031]
    ds_values = []
    for d in ds:
        ds_values.append(eval('sample.percent_finer_{0}mm'.format(d)))
    print(ds_values)
    # graph embbeded ina  div to return to the template:
    fig = go.Figure()

    # create graph
    fig.add_trace(go.Scatter(x=ds_float, y=ds_values,
                             mode='lines', name='test',
                             opacity=0.8,
                             #stackgroup='log'
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
    pass


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


