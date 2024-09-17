from django.urls import path
from rest_framework import routers

from checkout.views import CheckoutView, OrderListView

router = routers.DefaultRouter()

router.register(r"orders", OrderListView, basename="order-list")
urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]

urlpatterns += router.urls
