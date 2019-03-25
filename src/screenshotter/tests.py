import os
import magic
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from rest_framework.serializers import Serializer

from screenshotter.helpers import call_puppeteer
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
