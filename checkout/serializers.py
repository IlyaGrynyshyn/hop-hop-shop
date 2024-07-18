import datetime

from rest_framework import serializers

from checkout.models import Order, OrderItem


class CardInformationSerializer(serializers.Serializer):
    @staticmethod
    def validate_card_number(value):
        value = value.replace(" ", "")
        if not value.isdigit():
            raise serializers.ValidationError("Card number is invalid")
        if not 13 <= len(value) <= 19:
            raise serializers.ValidationError("Card number is invalid")
        return value

    @staticmethod
    def check_expiry_month(value):
        if not 1 <= int(value) <= 12:
            raise serializers.ValidationError("Invalid expiry month.")

    @staticmethod
    def check_expiry_year(value):
        today = datetime.datetime.now()
        if not int(value) >= today.year:
            raise serializers.ValidationError("Invalid expiry year.")

    @staticmethod
    def check_cvc(value):
        if not 3 <= len(value) <= 4:
            raise serializers.ValidationError("Invalid cvc number.")

    @staticmethod
    def check_payment_method(value):
        payment_method = value.lower()
        if payment_method not in ["card"]:
            raise serializers.ValidationError("Invalid payment_method.")

    card_number = serializers.CharField(
        max_length=150, required=True, validators=[validate_card_number]
    )
    expiry_month = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_month],
    )
    expiry_year = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_year],
    )
    cvc = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_cvc],
    )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderListSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "total_quantity", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    card_information = CardInformationSerializer(write_only=True)

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
            "card_information",
        ]
        write_only_fields = ["created_at", "updated_at", "paid"]
        read_only_fields = ["customer", "paid", "status"]

    def create(self, validated_data):
        card_information = validated_data.pop("card_information", None)
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        card_information = validated_data.pop("card_information", None)
        instance = super().update(instance, validated_data)
        return instance
