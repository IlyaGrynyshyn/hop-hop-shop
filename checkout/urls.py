from django.urls import path
from rest_framework import routers

from checkout.views import (
    CheckoutView,
    OrderListView,
    ProfileOrder,
    OrderStatisticsView,
)
from checkout.views import CheckoutView, OrderListView

router = routers.DefaultRouter()

router.register(r"orders", OrderListView, basename="order-list")
urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("order-statistics/", OrderStatisticsView.as_view(), name="order-statistics"),
    path("", CheckoutView.as_view(), name="checkout")
]

urlpatterns += router.urls
