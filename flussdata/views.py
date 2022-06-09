from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata
from flussdata.models import Freezecore


def home(request):
    return render(request, 'home.html')


def main(request):
    return render(request, 'flussdata/main.html')


# def table(request):
#     table_show = Freezecore.objects.all()
#     return render(request, 'flussdata/table.html', {'table_show': table_show})
