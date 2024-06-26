from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, ProductItemSerializer
from shop.models import Product
from cart.services import CartService


class CartDetailView(APIView):
    serializer_class = CartSerializer

    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            serializer_class = CartSerializer(cart)
            total_items = cart.item_count()
            total_price = cart.total_price()
            return Response(
                {
                    "products": serializer_class.data,
                    "total_price": total_price,
                    "total_items": total_items,
                },
                status=status.HTTP_200_OK,
            )
        else:
            cart = CartService(request)
            cart_items = list(cart)

            serialized_cart_items = []
            for item in cart_items:
                product_data = ProductItemSerializer(item["product"]).data
                item_data = {
                    "product": product_data,
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "total_price": item["total_price"],
                }
                serialized_cart_items.append(item_data)

            total_price = cart.get_total_price()
            total_items = cart.get_total_item()

            return Response(
                {
                    "products": serialized_cart_items,
                    "total_price": total_price,
                    "total_items": total_items,
                },
                status=status.HTTP_200_OK,
            )


class CartAddView(APIView):
    serializer_class = CartSerializer

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_authenticated:
            # TODO: implement save cart item in DB if user is authenticated
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
        else:
            cart = CartService(request)
            cart.add(
                product=product,
                quantity=request.data.get("quantity", 1),
                update_quantity=request.data.get("update_quantity", False),
            )
        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    serializer_class = CartSerializer

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if request.user.is_authenticated:
            # TODO: implement delete item from cart if user is authenticated
            ...
        else:
            cart = CartService(request)
            cart.remove(product)
            return Response(
                {"message": "Product removed from cart"}, status=status.HTTP_200_OK
            )
