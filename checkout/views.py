from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from checkout.serializers import OrderSerializer


from checkout.services import (
    OrderService,
    PaymentService,
)


class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_service = OrderService(request)
            payment_service = PaymentService()

            order_data = order_service.create_order(serializer.validated_data)
            response = payment_service.stripe_card_payment(
                order_data.card_information, order_data.total_price
            )
            print(response)
            if response.status_code == status.HTTP_200_OK:
                order_data.order.paid = True
                order_data.order.status = "Paid"
                order_data.order.save()
                order_service.clear_cart()

                return Response(
                    {
                        "order": serializer.data,
                        "message": "Order created and payment successful",
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                order_data.order.delete()
                return response
        raise ValidationError(serializer.errors)
