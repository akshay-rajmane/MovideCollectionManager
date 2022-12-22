from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from movie_collection.thirdparty import movies as movies_service
from movie_collection.helpers.response_helper import JSONResponse


class MoviesController:
    @staticmethod
    @api_view(["GET"])
    @login_required
    def get_movies(request):
        params = request.GET
        success, response = movies_service.get_movies(url=params.get("next"))
        kwargs = {
            "data": response,
            "status": 200 if success else 500
        }

        return JSONResponse(**kwargs)
