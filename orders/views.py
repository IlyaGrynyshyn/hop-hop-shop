from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )

        cart = get_object_or_404(Cart, user=request.user)
        if cart.items.count() == 0:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            for cart_item in cart.items.all():
                if cart_item.product.stock < cart_item.quantity:
                    return Response(
                        {"error": f"Not enough stock for {cart_item.product.name}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            cart.items.all().delete()

        return Response(
            {"success": "Order placed", "order_id": order.id}, status=status.HTTP_200_OK
        )
