from django.urls import path
from .views import (
    CartAddItemView,
    CartRemoveItemView,
    CartDetailView,
    CartSubtractItemView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<int:product_id>/", CartAddItemView.as_view(), name="cart_add"),
    path(
        "cart/remove/<int:product_id>/",
        CartRemoveItemView.as_view(),
        name="cart_remove",
    ),
    path(
        "cart/subtract/<int:product_id>/",
        CartSubtractItemView.as_view(),
        name="cart_subtract",
    ),
]
