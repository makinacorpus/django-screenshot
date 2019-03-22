from django.contrib import admin
from django.urls import path

from screenshotter.views import CaptureAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', CaptureAPIView.as_view(), name="capture"),
]
