from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from flussdata.views import
app_name = 'flussdata'

urlpatterns = [
    path('query', views.query, name='query'),
    path('modify', views.modify, name='modify'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('query/<int:id>/', views.view_sample, name='view_sample'),
    path('query/station<int:station_id>', views.station_data, name='station_data'),
    path('modify/upload/', views.upload_file, name='modify/upload'),
    path('modify/upload/success_upload/', views.success_upload, name='success_upload'),

    path('accounts/', include("django.contrib.auth.urls")),  # new
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
