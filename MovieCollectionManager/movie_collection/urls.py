from django.urls import path

from .views import (
    UserController,
    MoviesController,
    MovieCollectionController,
    RequestCounterController,
)

urlpatterns = [
    path('register/', UserController.register, name='register-new-user'),
    path('login/', UserController.login_user, name='login-user'),
    path('movies/', MoviesController.get_movies, name='get-movies'),
    path('collection/', MovieCollectionController.movie_collection, kwargs={'uuid': None}, name='manage-movies'),
    path('collection/<str:uuid>/', MovieCollectionController.movie_collection, name='manage-movies-by-uuid'),
    path('request-count/', RequestCounterController.get_request_count, name='get-request-count'),
    path('request-count/reset/', RequestCounterController.reset_request_count, name='reset-request-count'),
]
