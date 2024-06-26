from django.urls import path
from wishlist.views import (
    AddToWishlistView,
    RemoveFromWishlistView,
    WishlistView,
)

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlists"),
    path(
        "add/<int:product_id>/",
        AddToWishlistView.as_view(),
        name="add_to_wishlists",
    ),
    path(
        "remove/<int:product_id>/",
        RemoveFromWishlistView.as_view(),
        name="remove_from_wishlists",
    ),
]
