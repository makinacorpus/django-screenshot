from django.urls import path
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer
from rest_framework.schemas import get_schema_view

from . import views

app_name = 'screenshotter'

schema_view = get_schema_view(
    title='Screenshotter API',
    description='Common advanced chromium headless based API to get advanced screenshots from dynamic web pages',
    url='https://screenshotter.paas.kasta.ovh',
    renderer_classes=[JSONOpenAPIRenderer, BrowsableAPIRenderer],
    public=False,

)

urlpatterns = [
    path('capture/', views.CaptureAPIView.as_view(), name="capture"),
    path('', schema_view, name='schema'),
]
