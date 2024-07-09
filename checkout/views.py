from rest_framework import status, generics
from rest_framework.response import Response
from checkout.serializers import OrderSerializer


from checkout.services import create_order, stripe_card_payment



class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order, card_information, total_price = create_order(
                serializer.validated_data, request
            )
            response = stripe_card_payment(card_information, total_price)
            if response.status_code == status.HTTP_200_OK:
                order.paid = True
                order.status = "Pending"
                order.save()
                return Response(
                    {"order": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                order.delete()
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
