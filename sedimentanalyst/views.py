from django.shortcuts import render


def app(requests):
    return render(requests, 'sedimentanalyst/app.html')
