from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata


def home(request):
    return render(request, 'home.html')


def main(request):
    return render(request, 'flussdata/main.html')
