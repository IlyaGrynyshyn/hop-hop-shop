from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from authentication.views import (
    CreateCustomerView,
    ManageUserView,
    CustomTokenRefreshView,
    LoginView,
)

app_name: str = "authentication"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("registration/", CreateCustomerView.as_view(), name="create"),
    path("profile/", ManageUserView.as_view(), name="profile"),
]
