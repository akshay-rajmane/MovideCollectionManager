from django.test import TestCase

from movie_collection.models import CustomUser

class CustomUserTests(TestCase):

    def test_create_user(self):
        user = CustomUser(username="testuser", password="12345")
        user.save()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
