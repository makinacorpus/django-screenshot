from django.urls import path

from . import views

app_name = 'screenshotter'

urlpatterns = [
    path('capture/', views.CaptureAPIView.as_view(), name="capture"),
]
