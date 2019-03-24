from django.urls import path

from . import views

app_name = 'screenshotter'

urlpatterns = [
    path('', views.CaptureAPIView.as_view(), name="capture"),
]
