import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include('screenshotter.urls')),
]

if settings.DEBUG and os.getenv('DJANGO_SETTINGS_MODULE') == 'project.settings.dev':
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
