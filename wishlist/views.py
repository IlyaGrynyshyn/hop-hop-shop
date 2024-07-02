from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import WishlistService
from shop.models import Product
from .serializers import ProductSerializer


class AddToWishlistView(APIView):
    def post(self, request, product_id):
        service = WishlistService(request.session)
        try:
            product = service.add_product(product_id)
            return Response(
                {"product": ProductSerializer(product).data},
                status=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class RemoveFromWishlistView(APIView):
    def post(self, request, product_id):
        service = WishlistService(request.session)
        try:
            service.remove_product(product_id)
            return Response(status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ViewWishlistView(APIView):
    def get(self, request):
        service = WishlistService(request.session)
        products = service.get_products()
        serialized_products = ProductSerializer(products, many=True).data
        return Response({"products": serialized_products}, status=status.HTTP_200_OK)


class ClearWishlistView(APIView):
    def post(self, request):
        service = WishlistService(request.session)
        service.clear()
        return Response(status=status.HTTP_200_OK)
