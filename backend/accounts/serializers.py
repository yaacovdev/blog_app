from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.

    This serializer is used to serialize and deserialize User objects.
    It includes fields for username, password, and email.

    Attributes:
        password (CharField): A write-only field for the user's password.
        email (EmailField): A required field for the user's email address.

    Meta:
        model (User): The User model that this serializer is associated with.
        fields (list): The fields to include in the serialized representation.

    Methods:
        create(validated_data): Creates a new User object based on the validated data.

    """

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        """
        Create a new User object.

        This method creates a new User object based on the validated data.
        It uses the `create_user` method of the User model to create the user.

        Args:
            validated_data (dict): The validated data containing the user's username, password, and email.

        Returns:
            User: The newly created User object.

        """
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user
