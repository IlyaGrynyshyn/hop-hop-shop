from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet
from wishlist.views import (
    add_to_wishlist,
    remove_from_wishlist,
    view_wishlist,
    clear_wishlist,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/add-to-wishlist/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"
    ),
    path(
        "api/remove-from-wishlist/<int:product_id>/",
        remove_from_wishlist,
        name="remove_from_wishlist",
    ),
    path("api/view-wishlist/", view_wishlist, name="view_wishlist"),
    path("api/clear-wishlist/", clear_wishlist, name="clear_wishlist"),
]
