from base64 import b64encode

from rest_framework.response import Response
from rest_framework.views import APIView

from screenshotter.helpers import call_puppeteer
from screenshotter.serializer import ScreenshotSerializer


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
