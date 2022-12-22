from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class UserAPITests(APITestCase):

    def test_user_register(self):
        request_data = {}
        api_client = APIClient()
        response = api_client.post(reverse('register-new-user'), data=request_data)
        self.assertEquals(response.status_code, 400)
        request_data['username'] = 'testuser'
        response = api_client.post(reverse('register-new-user'), data=request_data)
        self.assertEquals(response.status_code, 400)
        request_data['password'] = '1234'
        response = api_client.post(reverse('register-new-user'), data=request_data)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.json().get("access_token"))
