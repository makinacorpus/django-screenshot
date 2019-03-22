from django.contrib import admin
from django.urls import path, include

from screenshotter.views import CaptureAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('screenshotter.urls', namespace='screenshotter')),
]
