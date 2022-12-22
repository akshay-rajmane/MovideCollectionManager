from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from MovieCollectionManager.settings import REQUEST_COUNT_CACHE_KEY
from movie_collection.helpers.response_helper import JSONResponse

@api_view(["GET"])
@login_required
def get_request_count(request):
    return JSONResponse(
        data={'requests': cache.get(REQUEST_COUNT_CACHE_KEY, 0)},
        status=200
    )


@api_view(["POST"])
@login_required
def reset_request_count(request):
    cache.set(REQUEST_COUNT_CACHE_KEY, 0, timeout=None)
    return JSONResponse(
        data={'message': "Request count reset successfully"},
        status=200
    )
