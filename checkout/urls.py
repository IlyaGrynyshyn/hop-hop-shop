from django.urls import path
from rest_framework import routers

from checkout.views import CheckoutView, OrderListView, ProfileOrder

router = routers.DefaultRouter()

router.register(r"orders", OrderListView, basename="order-list")
router.register(r"profile", ProfileOrder, basename="profile-order")

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]

urlpatterns += router.urls
