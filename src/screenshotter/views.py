from base64 import b64encode

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
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
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                png = call_puppeteer(**serializer.validated_data)
                response = {'base64': b64encode(png)}
                status = HTTP_200_OK
            except Exception as exc:
                response = {'errors': f'{exc}'}
                status = HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response = {'errors': serializer.errors}
            status = HTTP_400_BAD_REQUEST

        return Response(response, status=status)
