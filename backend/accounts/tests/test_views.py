from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..serializers import UserSerializer


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """
        Test that a new user can be registered successfully.
        """
        url = reverse("register")
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")
        self.assertEqual(User.objects.get().email, "test@example.com")
        self.assertTrue("token" in response.data)
        self.assertTrue("user" in response.data)
        self.assertEqual(response.data["user"], UserSerializer(User.objects.get()).data)
        self.assertEqual(
            response.data["token"], Token.objects.get(user=User.objects.get()).key
        )

    def test_register_user_invalid_data(self):
        """
        Test that registration fails with invalid data.
        """
        url = reverse("register")
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertFalse("token" in response)
        self.assertFalse("user" in response)
