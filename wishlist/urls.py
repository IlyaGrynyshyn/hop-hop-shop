from django.urls import path
from . import views


urlpatterns = [
    path(
        "add-to-wishlist/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),
    path(
        "remove-from-wishlist/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
    path("view-wishlist/", views.view_wishlist, name="view_wishlist"),
    path("clear-wishlist/", views.clear_wishlist, name="clear_wishlist"),
]
