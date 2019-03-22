from django.contrib import admin
from django.urls import path

from screenshotter.views import CaptureView, CaptureAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('capture/', CaptureAPIView.as_view()),
    path('', CaptureView.as_view(), name='capture'),
]
