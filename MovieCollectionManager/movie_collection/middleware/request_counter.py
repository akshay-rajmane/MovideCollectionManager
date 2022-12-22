from django.core.cache import cache
from MovieCollectionManager.settings import REQUEST_COUNT_CACHE_KEY
def request_counter_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        cache.set(REQUEST_COUNT_CACHE_KEY, cache.get(REQUEST_COUNT_CACHE_KEY, 0) + 1, timeout=None)
        print("request_counter~:", cache.get(REQUEST_COUNT_CACHE_KEY, 0))
        return response
    return middleware