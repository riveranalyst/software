from django.urls import path
from . import views
# from riveranalyst.sedimentanalyst import web_application

app_name = 'sedimentanalyst'

urlpatterns = [
    path('', views.app, name='app')
]