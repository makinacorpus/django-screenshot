import json
import subprocess
from tempfile import NamedTemporaryFile

from django.conf import settings


def call_puppeteer(url, viewport_width=1920, viewport_height=1080, wait_selectors=(), selector='body', forward_headers=None):
    if forward_headers is None:
        forward_headers = dict()
    screenshot_file = NamedTemporaryFile(suffix='.png')

    with open(screenshot_file.name, 'w+b'):
        subprocess.run([
            'node',
            settings.PUPPETEER_JAVASCRIPT_FILEPATH,
            '-u',
            url,
            json.dumps(wait_selectors),
            selector,
            screenshot_file.name,
            json.dumps(forward_headers)
        ])

    with open(screenshot_file.name, 'rb') as screenshot_data:
        return screenshot_data.read()


