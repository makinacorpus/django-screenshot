import os
import magic
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.serializers import Serializer
from rest_framework.test import APIClient

from screenshotter.helpers import call_puppeteer
from screenshotter.serializer import ScreenshotSerializer
from screenshotter.views import CaptureAPIView

temp_dir = TemporaryDirectory()


class CaptureTestCase(TestCase):
    @override_settings(MEDIA_ROOT=temp_dir.name)
    def test_capture_mime(self):
        png = call_puppeteer('https://www.google.fr')

        png_path = os.path.join(temp_dir.name, 'test.png')
        cfile = ContentFile(content=png)
        default_storage.save(name=png_path, content=cfile)


        self.assertTrue(os.path.exists(png_path))

        self.assertNotEqual(os.path.getsize(png_path), 0)

        mime = magic.from_file(png_path, mime=True)
        self.assertEqual(mime, "image/png", )

    @override_settings(MEDIA_ROOT=temp_dir.name)
    def test_capture_size(self):
        png = call_puppeteer('https://www.google.fr', viewport_width=1280, viewport_height=720)

        png_path = os.path.join(temp_dir.name, 'test2.png')
        cfile = ContentFile(content=png)
        default_storage.save(name=png_path, content=cfile)

        image = Image.open(png_path)

        self.assertEqual(image.width, 1280)
        self.assertEqual(image.height, 720)

    def test_bad_dns(self):
        with self.assertRaises(Exception):
            call_puppeteer('https://cccccc')

    def test_view_has_get_serializer(self):
        view = CaptureAPIView()

        self.assertTrue(hasattr(view, 'get_serializer'))
        self.assertTrue(isinstance(view.get_serializer(), Serializer))


class CaptureApiTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create(username='test')
        self.api_client.force_login(self.user)

    def test_api_good_request(self):
        serializer = ScreenshotSerializer()
        data = serializer.data
        data['url'] = "https://www.google.fr"

        response = self.api_client.post(reverse('screenshotter:capture'), data=data, format='json')
        self.assertEqual(response.status_code, 200, serializer.data)

    def test_api_bad_request(self):
        serializer = ScreenshotSerializer()
        response = self.api_client.post(reverse('screenshotter:capture'), data=serializer.data, format='json')
        self.assertEqual(response.status_code, 400, serializer.data)

    def test_api_wrong_response(self):
        serializer = ScreenshotSerializer()
        data = serializer.data
        data['url'] = "https://kikou.com"
        response = self.api_client.post(reverse('screenshotter:capture'), data=data, format='json')
        self.assertEqual(response.status_code, 500, response.json())
