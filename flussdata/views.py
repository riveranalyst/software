from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata
from flussdata.models import Freezecore
import flussdata.tables as flutb
from .filters import OrderFilter


def home(request):
    return render(request, 'home.html')


def query(request):

    return render(request, 'flussdata/query.html')


def modify(request):
    return render(request, 'flussdata/modify.html')


def table(request):
    #  Get all measurement data from the table
    freezecore_objects = Freezecore.objects.all()

    # Get filter if the user selected any
    myFilter = OrderFilter(request.GET, queryset=freezecore_objects)

    # Apply filter, remaking the object
    freezecore_objects = myFilter.qs

    # Shows the table
    table_show = flutb.FreezecoreTable(freezecore_objects)

    #  return this to the context
    context = {'table_show': table_show, 'myFilter': myFilter}

    return render(
        request,
        'flussdata/table.html', context)


