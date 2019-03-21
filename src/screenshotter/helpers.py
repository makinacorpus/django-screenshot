import json
import subprocess
from tempfile import NamedTemporaryFile


def call_puppeteer(url, width=1920, height=1080, wait_selectors=(), selector='body', headers={}):
    screenshot_file = NamedTemporaryFile(suffix='.png')
    headers = {
        'Authorization': 'Basic amVjOmplY2plYzQ2'
    }
    with open(screenshot_file.name, 'w+b'):
        subprocess.run([
            'node',
            '/app/src/index.js',
            '-u',
            url,
            selector,
            selector,
            screenshot_file.name,
            json.dumps(headers)
        ])

    with open(screenshot_file.name, 'rb') as screenshot_data:
        return screenshot_data.read()
