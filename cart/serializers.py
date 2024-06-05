from rest_framework import serializers
from cart.models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    item_total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "added_at", "item_total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "session_key",
            "created_at",
            "updated_at",
            "items",
            "total_price",
            "item_count",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "updated_at", "status", "items"]
