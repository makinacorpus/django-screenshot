import json
import subprocess
from tempfile import NamedTemporaryFile

from django.conf import settings


def call_puppeteer(url, width=1920, height=1080, wait_selectors=(), selector='body', headers={}):
    screenshot_file = NamedTemporaryFile(suffix='.png')

    with open(screenshot_file.name, 'w+b'):
        subprocess.run([
            'node',
            settings.PUPPETEER_JAVASCRIPT_FILEPATH,
            '-u',
            url,
            selector,
            selector,
            screenshot_file.name,
            json.dumps(headers)
        ])

    with open(screenshot_file.name, 'rb') as screenshot_data:
        return screenshot_data.read()



