from django.urls import path
from .views import (
    AddToFavouritesView,
    RemoveFromFavouritesView,
    ViewFavouritesView,
    ClearFavouritesView,
)

urlpatterns = [
    path(
        "favourites/add/<int:product_id>/",
        AddToFavouritesView.as_view(),
        name="add_to_favourites",
    ),
    path(
        "favourites/remove/<int:product_id>/",
        RemoveFromFavouritesView.as_view(),
        name="remove_from_favourites",
    ),
    path("favourites/", ViewFavouritesView.as_view(), name="view_favourites"),
    path("favourites/clear/", ClearFavouritesView.as_view(), name="clear_favourites"),
]
