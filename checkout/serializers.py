from rest_framework import serializers
from checkout.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "first_name",
            "last_name",
            "email",
            "phone",
            "paid",
            "created_at",
            "updated_at",
            "status",
            "items",
        ]
        write_only_fields = ["created_at", "updated_at", "paid"]
        read_only_fields = ["customer"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
