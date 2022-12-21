from django.test import TestCase

from django.contrib.auth.models import User
from movie_collection.repositories.user import get_auth_token

class UserTests(TestCase):

    def test_create_user(self):
        user = User(username="testuser", password="12345")
        user.save()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_auth_token_generation(self):
        user = User(username="testuser", password="12345")
        user.save()
        token = get_auth_token(user)
        self.assertIsNotNone(token)
        # Test if existing token is fetched
        token = get_auth_token(user)
