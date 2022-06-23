from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'flussdata'

urlpatterns = [
    path('query', views.query, name='query'),
    path('modify', views.modifyView.as_view(), name='modify'),
    # path('table', views.table, name='table')
    path('query/<int:id>/', views.view_sample),
    path('modify/upload', views.file_upload_view, name='modify/upload')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
