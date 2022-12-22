from typing import Tuple

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken




def get_auth_token(user: User) -> str:
    """ Generates JWT auth token for given User obj """

    token = RefreshToken.for_user(user)
    return str(token.access_token)


def register(username: str, password: str) -> Tuple[bool, str]:
    """ Registers a new user and returns access token """

    if User.objects.filter(username=username).exists():
        return False, "Username already exists. Please select another username or login"

    user = User.objects.create(username=username, password=password)
    user.set_password(password)
    user.save()
    return True, get_auth_token(user=user)


def login_user(username: str, password: str) -> Tuple[bool, str]:
    """ Logs in an resgisterd user """

    user = authenticate(username=username, password=password)
    if not user:
        return False, "Invalid credentials"

    return True, get_auth_token(user=user)
