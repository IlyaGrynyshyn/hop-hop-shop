from rest_framework import serializers

from cart.services import CartSessionService
from checkout.models import Order, OrderItem
from shop.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "first_name",
            "last_name",
            "email",
            "phone",
            "shipping_country",
            "shipping_city",
            "shipping_address",
            "shipping_postcode",
            "paid",
            "status",
            "items",
        ]
        write_only_fields = ["created_at", "updated_at", "paid"]
        read_only_fields = ["customer"]

    def create(self, validated_data):
        request = self.context.get("request")
        cart = CartSessionService(request)

        items_data = [
            {
                "product": Product.objects.get(id=item["product"]["id"]),
                "quantity": item["quantity"],
                "price": item["price"],
            }
            for item in cart
        ]

        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        cart.clear()
        return order
