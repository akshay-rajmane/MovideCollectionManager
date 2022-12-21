from django.http.response import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """JSON response class for view(controller) return values"""

    def __init__(self, data: dict, **kwargs):
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content, content_type="application/json", **kwargs)
