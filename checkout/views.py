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

        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
