from django.urls import path
from cart.views import AddToCartView, UpdateCartView, CartView, RemoveFromCartView

urlpatterns = [
    path("", CartView.as_view(), name="cart_detail"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("update/<int:item_id>/", UpdateCartView.as_view(), name="update_cart"),
    path(
        "remove/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
]
