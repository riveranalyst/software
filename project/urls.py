"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.views.defaults import permission_denied

# added app views:
from riveranalyst import views as river_views

urlpatterns = [
    path('', river_views.home, name='home'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),  # MUST come before path(admin)
    path('admin/', admin.site.urls),
    path('riveranalyst/', include('riveranalyst.urls')),
    path('sedimentanalyst/', include('sedimentanalyst.urls')),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    *static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]),
    # Serve static files from the app's static directory
    path('static/examples', serve, {'document_root': 'static'}),
    ]

