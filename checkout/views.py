from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from checkout.tasks.order_notification import send_notification_mail

from checkout.models import Order
from checkout.serializers import OrderSerializer, OrderListSerializer
from checkout.services import (
    OrderService,
    PaymentService,
)
from utils.pagination import Pagination


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
            if response.status_code == status.HTTP_200_OK:
                order_data.order.paid = True
                order_data.order.status = "Paid"
                order_data.order.save()
                send_notification_mail.delay(user_email=order_data.order.email)
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


@extend_schema(tags=["orders"], summary="Get all orders")
class OrderListView(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = Pagination

    queryset = Order.objects.all().select_related("customer")
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    @extend_schema(
        summary="Retrieve a list of orders",
        description="This endpoint returns a list of all orders.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an order by ID",
        description="This endpoint returns details of a specific order identified by its ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an order",
        description="This endpoint allows you to partially update an existing order.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an order",
        description="This endpoint allows you to delete an existing order.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
