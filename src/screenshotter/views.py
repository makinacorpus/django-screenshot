from django.http import HttpResponse
from django.views import View
from screenshotter.helpers import call_puppeteer


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
            png = call_puppeteer(url, width=width, height=height, wait_selectors=wait_selectors, selector=selector, headers=headers)
            return HttpResponse(png, content_type="image/png", status=200)

        except Exception as exc:
            return HttpResponse(str(exc), status=500)
