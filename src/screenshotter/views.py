from base64 import b64encode

from django.http import HttpResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from screenshotter.helpers import call_puppeteer
from screenshotter.serializer import ScreenshotSerializer


def clean_url(url):
    if not url:
        raise Exception('missing url parameter')

    return url


class CaptureView(View):
    def get(self, request, *args, **kwargs):
        try:
            url = clean_url(request.GET.get('url'))
            wait_selectors = request.GET.getlist('wait')
            selector = request.GET.get('selector', 'body')
            width, height = [1920, 1080]
            headers = {
                'Authorization': 'Basic amVjOmplY2plYzQ2'
            }
            png = call_puppeteer(url, viewport_width=width, viewport_height=height, wait_selectors=wait_selectors,
                                 selector=selector, forward_headers=headers)
            return HttpResponse(png, content_type="image/png", status=200)

        except Exception as exc:
            return HttpResponse(str(exc), status=500)


class CaptureAPIView(APIView):
    serializer_class = ScreenshotSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Keep this method to see json structure in API html view
        """
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(data=request.data)

        if self.serializer.is_valid():
            png = call_puppeteer(**self.serializer.validated_data)
            response = {'base64': b64encode(png)}

        else:
            response = {'errors': self.serializer.errors}

        return Response(response)
