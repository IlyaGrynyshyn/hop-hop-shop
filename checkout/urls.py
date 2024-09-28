from django.urls import path
from rest_framework import routers

from checkout.views import (
    CheckoutView,
    OrderListView,
    ProfileOrder,
    OrderStatisticsView,
)

router = routers.DefaultRouter()

router.register(r"orders", OrderListView, basename="order-list")
router.register(r"profile", ProfileOrder, basename="profile-order")

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("order-statistics/", OrderStatisticsView.as_view(), name="order-statistics"),
]

urlpatterns += router.urls
