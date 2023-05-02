from django.urls import path
from . import views
from sedimentanalyst.app import web_application

app_name = 'sedimentanalyst'

urlpatterns = [
    path('', views.app, name='app'),
]