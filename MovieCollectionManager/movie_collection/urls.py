from django.urls import path

from .views import UserController, MoviesController

urlpatterns = [
    path('register/', UserController.register, name='register-new-user'),
    path('login/', UserController.login_user, name='login-user'),
    path('movies/', MoviesController.get_movies, name='get-movies'),
]
