from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from wishlist.services import WishlistService
from shop.models import Product
from utils.custom_exceptions import (
    ProductAlreadyExistException,
    ProductNotExistException,
)


@extend_schema(summary="Retrieve wishlist details")
class WishlistView(APIView):
    def get(self, request):
        products = WishlistService(request)
        return Response({"products": products}, status=status.HTTP_200_OK)


@extend_schema(summary="Add item to wishlist")
class AddToWishlistView(APIView):
    def post(self, request, product_id):
        wishlist_service = WishlistService(request)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            wishlist_service.add(product=product)
        except ProductAlreadyExistException as error:
            return Response(
                {"error": error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(wishlist_service, status=status.HTTP_200_OK)


@extend_schema(summary="Remove item from wishlist")
class RemoveFromWishlistView(APIView):
    def delete(self, request, product_id):
        wishlist_service = WishlistService(request)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            wishlist_service.remove(product=product)
        except ProductNotExistException as error:
            return Response({"error": error.message}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
