from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..serializers import UserSerializer


class UserSerializerTest(APITestCase):
    def test_create_user(self):
        """
        Test that a new User object is created correctly.
        """
        serializer = UserSerializer()
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
        }
        user = serializer.create(data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_serializer_fields(self):
        """
        Test that the serializer includes the correct fields.
        """
        serializer = UserSerializer()
        expected_fields = ["username", "password", "email"]
        self.assertEqual(list(serializer.fields.keys()), expected_fields)

    def test_bad_serializer_data(self):
        """
        Test that the serializer raises an error for bad data.
        """
        serializer = UserSerializer()
        data = {
            "username": "testuser",
            "email": "",
        }
        with self.assertRaises(Exception):
            serializer.create(data)
