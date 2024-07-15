from django.urls import path
from authentication.views import (
    CreateCustomerView,
    ManageUserView,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name: str = "authentication"
urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("registration/", CreateCustomerView.as_view(), name="create"),
    path("profile/", ManageUserView.as_view(), name="profile"),
]
