from django.shortcuts import render


def app(requests):
    context = {'navbar': 'activesed'}
    return render(requests, 'sedimentanalyst/app.html', context)
