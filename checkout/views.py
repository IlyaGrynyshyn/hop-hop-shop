from rest_framework import generics, status
from rest_framework.response import Response
from checkout.serializers import OrderSerializer
from cart.services import CartSessionService


class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        cart = CartSessionService(request)
        if not len(cart):
            return Response(
                {"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        items_data = [
            {
                "product": item["product"]["id"],
                "quantity": item["quantity"],
                "price": item["price"],
            }
            for item in cart
        ]
        order_data = {**request.data, "items": items_data}
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            cart.clear()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        cart = CartSessionService(self.request)

        items_data = [
            {
                "product": item["product"]["id"],
                "quantity": item["quantity"],
                "price": item["price"],
            }
            for item in cart
        ]

        serializer.save(items=items_data)
