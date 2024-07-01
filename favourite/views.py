from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import FavouriteService
from shop.models import Product
from .serializers import ProductSerializer


class AddToFavouritesView(APIView):
    def post(self, request, product_id):
        service = FavouriteService(request.session)
        try:
            product = service.add_product(product_id)
            return Response(
                {"success": True, "product": ProductSerializer(product).data},
                status=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return Response(
                {"success": False, "error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class RemoveFromFavouritesView(APIView):
    def post(self, request, product_id):
        service = FavouriteService(request.session)
        try:
            product = service.remove_product(product_id)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"success": False, "error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ViewFavouritesView(APIView):
    def get(self, request):
        service = FavouriteService(request.session)
        products = service.get_products()
        serialized_products = ProductSerializer(products, many=True).data
        return Response({"products": serialized_products}, status=status.HTTP_200_OK)


class ClearFavouritesView(APIView):
    def post(self, request):
        service = FavouriteService(request.session)
        service.clear()
        return Response({"success": True}, status=status.HTTP_200_OK)
