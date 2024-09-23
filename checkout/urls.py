from django.urls import path
from rest_framework import routers

from checkout.views import CheckoutView, OrderListView, AlternativeCheckoutView

router = routers.DefaultRouter()

router.register(r"orders", OrderListView, basename="order-list")
urlpatterns = [
    path("card/", CheckoutView.as_view(), name="checkout"),
    path("other/", AlternativeCheckoutView.as_view(), name="checkout-alternative"),
]

urlpatterns += router.urls
