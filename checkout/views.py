from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from checkout.filters import OrderFilter
from checkout.tasks.order_notification import send_notification_mail

from checkout.models import Order
from checkout.serializers import OrderSerializer, OrderListSerializer
from checkout.services import (
    OrderService,
    PaymentService,
)
from utils.pagination import Pagination


@extend_schema(tags=["checkout"], summary="Checkout for specific payment method")
class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            order_service = OrderService(request)
            order_data = order_service.create_order(serializer.validated_data)
            serializer.validated_data["order_id"] = order_data.order.id

            payment_id = None
            if serializer.validated_data.get('payment_type', None) == 'card':
                payment_service = PaymentService()

                response = payment_service.stripe_card_payment(
                    order_data.card_information, order_data.total_price
                )

                if response.status_code != status.HTTP_200_OK:
                    order_data.order.payment_status = "Failed"
                    return response
                else:
                    payment_id = response.data.get("payment_id")

            order_data.order.payment_status = "pending"
            order_data.order.payment_id = payment_id
            order_data.order.save()

            # send_notification_mail.delay(user_email=order_data.order.email)

            order_service.clear_cart()

            return Response(
                {
                    "order": serializer.validated_data,
                    "payment_id": payment_id,
                    "message": "Order created and payment successful",
                    "sessionid": request.session.get("session_key", None),
                },
                status=status.HTTP_201_CREATED,
            )


@extend_schema(tags=["orders"], summary="Get all orders")
class OrderListView(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = Pagination
    filterset_class = OrderFilter

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
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Order deleted successfully."}, status=status.HTTP_200_OK
        )
