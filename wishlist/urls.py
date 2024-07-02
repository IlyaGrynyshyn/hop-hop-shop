from django.urls import path
from .views import (
    AddToWishlistView,
    RemoveFromWishlistView,
    ViewWishlistView,
)

urlpatterns = [
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
    path("", ViewWishlistView.as_view(), name="view_wishlists"),
]
