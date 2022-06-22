from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata
from flussdata.models import Freezecore
import flussdata.tables as flutb
from .filters import TableFilter
from .forms import *
from alter_tables import *
from django.core.files.storage import FileSystemStorage


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

    # Shows the table
    table_show = flutb.FreezecoreTable(freezecore_objects)

    #  return this to the context
    context = {'myFilter': myFilter, 'table_show': table_show, 'title': 'Flussdata: Query', 'navbar': 'activequery'}

    return render(request, 'flussdata/query.html', context)


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
            message = "Something went wrong while updating database table, check your columns names."
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


