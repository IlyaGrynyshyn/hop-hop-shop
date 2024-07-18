from django.urls import path
from cart.views import (
    CartAddItemView,
    CartRemoveItemView,
    CartDetailView,
    CartSubtractItemView,
    UseCouponView,
    RemoveCouponView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:product_id>/", CartAddItemView.as_view(), name="cart_add"),
    path(
        "remove/<int:product_id>/",
        CartRemoveItemView.as_view(),
        name="cart_remove",
    ),
    path(
        "subtract/<int:product_id>/",
        CartSubtractItemView.as_view(),
        name="cart_subtract",
    ),
    path("coupon/", UseCouponView.as_view(), name="coupon"),
    path("coupon/remove/", RemoveCouponView.as_view(), name="coupon_remove"),
]
