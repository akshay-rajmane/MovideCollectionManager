from rest_framework.decorators import api_view

from movie_collection.repositories import user as user_repo
from movie_collection.helpers.response_helper import JSONResponse


class UserController:
    @staticmethod
    @api_view(["POST"])
    def register(request):
        request_data = request.data
        if not request_data.get('username') or not request_data.get('password'):
            return JSONResponse(
                data={'message': 'Username and Password are required'},
                status=400
            )

        success, response = user_repo.register(
            username=request_data.get('username'),
            password=request_data.get('password'),
        )
        if not success:
            return JSONResponse(
                data={'message': 'Unable to register, please try again'},
                status=500
            )

        return JSONResponse(
                data={'access_token': response},
                status=200
            )


    @staticmethod
    @api_view(["POST"])
    def login_user(request):
        request_data = request.data
        if not request_data.get('username') or not request_data.get('password'):
            return JSONResponse(
                data={'message': 'Username and Password are required'},
                status=400
            )

        success, response = user_repo.login_user(
            username=request_data.get('username'),
            password=request_data.get('password'),
        )
        if not success:
            return JSONResponse(
                data={'message': 'Invalid credentials'},
                status=401
            )

        return JSONResponse(
                data={'access_token': response},
                status=200
            )
