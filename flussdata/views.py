from django.shortcuts import render
from django.http import HttpResponse  # added for flussdata


def home(request):
    print('\n\nRequest object:', request)
    print('Request object type:', type(request), '\n\n')
    html_tags = '''
    <h1>This is the Home Page</h1>
    <h3>Thanks for visiting us</h3>
    <p> MVT means: </p>
    <ul>
        <li>Model</li>
        <li>View</li>
        <li>Template</li>
    </ul>
    '''
    response = HttpResponse(html_tags)
    print('Response object:', response)
    print('Responde object type:', type(response))
    print('\n\nUser-agent info:', end='')
    print(request.META['HTTP_USER_AGENT'], '\n\n')

    return response


def main(request):
    message = '<h1>This is the flussdata MAIN page.</h1>'
    return HttpResponse(message)


def user_info(request):
    message = '<h1>This is the films USER_INFO page.</h1>'
    return HttpResponse(message)