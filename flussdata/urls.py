from django.urls import path
from . import views

app_name = 'flussdata'

urlpatterns = [
    path('', views.main, name='main'),
]
