from django.urls import path

from authentication.views import (
    CreateCustomerView,
    CustomerProfileView,
    CustomTokenRefreshView,
    LoginView,
    LogoutView,
    CustomersListView,
)

app_name: str = "authentication"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("registration/", CreateCustomerView.as_view(), name="create"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", CustomerProfileView.as_view(), name="profile"),
    path("customers/", CustomersListView.as_view(), name="customers"),
]
