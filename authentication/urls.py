from django.urls import path
from authentication.views import (
    CreateCustomerView,
    ManageUserView,
)


app_name: str = "customer"
urlpatterns = [
    path("registration/", CreateCustomerView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
