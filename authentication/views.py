from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.models import Customer
from authentication.serializers import (
    CustomerSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
)
from utils.custom_exceptions import InvalidCredentialsError


@extend_schema(tags=["authentication"], summary="Registering a new user")
class CreateCustomerView(generics.CreateAPIView):
    """
    API view to register a new user.

    This view handles the creation of a new user account. Upon successful registration,
    it issues JWT tokens (access and refresh) and sets the refresh token in an HTTP-only cookie.

    """

    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs) -> Response:
        """
        Handle the creation of a new user and issue JWT tokens.

         Args:
            request: The HTTP request object containing user registration data.

        Returns:
            Response: The HTTP response object containing user data and JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response(status=status.HTTP_201_CREATED)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=refresh,
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.data = {
                "user": CustomerSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return response


@extend_schema(tags=["authentication"], summary="Log in to an existing account")
class LoginView(APIView):
    """
    API view to log in an existing user.

    This view handles user authentication and issues JWT tokens upon successful login.
    The refresh token is set in an HTTP-only cookie.

    Methods:
        post: Handles POST requests to log in a user.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle user login and issue JWT tokens.

        Args:
            request: The HTTP request object containing login credentials.

        Returns:
            Response: The HTTP response object containing user data and access token.

        Raises:
            InvalidCredentialsError: If the login credentials are invalid.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response()
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=refresh,
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.data = {
                "user": CustomerSerializer(user).data,
                "access": str(refresh.access_token),
            }
            return response
        raise InvalidCredentialsError


@extend_schema(tags=["authentication"])
class CustomTokenRefreshView(TokenRefreshView):
    """
    API view to refresh JWT tokens using refresh token from cookie
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        request.data["refresh"] = refresh_token
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["customer data"], summary="Get all customers")
class CustomersListView(generics.ListAPIView):
    """
    API view to list all customers.
    """

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


@extend_schema(tags=["customer data"], summary="Get information about your profile")
class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update the authenticated user's profile.
    """

    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordViewSet(generics.UpdateAPIView):
    queryset = get_user_model()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
