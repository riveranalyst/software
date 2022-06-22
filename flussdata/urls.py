from django.urls import path
from . import views

app_name = 'flussdata'

urlpatterns = [
    path('query', views.query, name='query'),
    path('modify', views.modify, name='modify'),
    # path('table', views.table, name='table')
    path('query/<int:id>/', views.view_sample),
]
