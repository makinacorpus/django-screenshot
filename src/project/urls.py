from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from screenshotter.views import CaptureView

urlpatterns = [
    path('', CaptureView.as_view(), name='capture'),
]

#if settings.DEBUG:
#    urlpatterns.append(static(settings.MEDIA_URL, document_root=settings.MEDIA_URL_ROOT))
