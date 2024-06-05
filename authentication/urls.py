from django.urls import path
from authentication.views import (
    CreateCustomerView,
    ManageUserView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name: str = "customer"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("registration/", CreateCustomerView.as_view(), name="create"),
    path("profile/", ManageUserView.as_view(), name="profile"),
]
