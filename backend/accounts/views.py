from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import UserSerializer


from rest_framework.authtoken.models import Token


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows users to register by creating a new account.
    Upon successful registration, a user object and an authentication token are returned.

    Inherits from `generics.CreateAPIView` which provides the default implementation for creating objects.

    Attributes:
        queryset (QuerySet): The queryset of User objects.
        permission_classes (list): The list of permission classes applied to the view.
        serializer_class (Serializer): The serializer class used for serializing and deserializing User objects.

    Methods:
        create(request, *args, **kwargs): Overrides the default implementation to handle user registration.

    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.

        This method is called when a POST request is made to the view.
        It validates the request data, creates a new user object, generates an authentication token,
        and returns the user object and token in the response.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the user object and token.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token.key,
            }
        )
