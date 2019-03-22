from django.urls import path

from screenshotter.views import CaptureView, CaptureAPIView

urlpatterns = [
    path('', CaptureView.as_view(), name='capture'),
    path('capture/', CaptureAPIView.as_view()),
]
