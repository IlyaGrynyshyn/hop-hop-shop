import datetime
from decimal import Decimal

from rest_framework import serializers

from cart.models import Coupon
from checkout.models import Order, OrderItem
from shop.models import Product
from shop.serializers import ProductSerializer


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
    product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "product_id",
            "product_name",
            "product_price",
            "quantity",
            "total_price",
        ]

    def get_product_id(self, obj):
        return obj.product_id

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_price(self, obj):
        return float(obj.price)

    def get_total_price(self, obj):
        return obj.price * obj.quantity


class OrderListSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())

    class Meta:
        model = Order
        fields = [
            "id",
            "payment_status",
            "order_status",
            "created_at",
            "total_quantity",
            "total_price",
        ]


class OrderSerializerMixin(serializers.ModelSerializer):
    def get_subtotal_price(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())

    def get_discount(self, obj):
        if obj.coupon:
            return obj.coupon.discount

    def get_total_price(self, obj):
        discount = self.get_discount(obj)
        subtotal_price = self.get_subtotal_price(obj)
        if discount:
            return subtotal_price - (subtotal_price * Decimal(discount / 100))
        return subtotal_price

    def create(self, validated_data):
        validated_data.pop("card_information", None)
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        validated_data.pop("card_information", None)
        instance = super().update(instance, validated_data)
        return instance


class OrderSerializer(OrderSerializerMixin):
    items = OrderItemSerializer(many=True, read_only=True)
    card_information = CardInformationSerializer(write_only=True)
    subtotal_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "customer",
            "first_name",
            "last_name",
            "email",
            "phone",
            "shipping_country",
            "shipping_city",
            "shipping_address",
            "shipping_postcode",
            "payment_id",
            "payment_type",
            "payment_status",
            "order_status",
            "items",
            "subtotal_price",
            "total_price",
            "coupon",
            "discount",
            "card_information",
        ]
        read_only_fields = [
            "customer",
            "coupon",
            "payment_id",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "PATCH":
            self.fields.pop("card_information", None)


class AlternativeOrderSerializer(OrderSerializerMixin):
    items = OrderItemSerializer(many=True, read_only=True)
    subtotal_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "customer",
            "first_name",
            "last_name",
            "email",
            "phone",
            "shipping_country",
            "shipping_city",
            "shipping_address",
            "shipping_postcode",
            "payment_type",
            "payment_status",
            "order_status",
            "items",
            "subtotal_price",
            "total_price",
            "coupon",
            "discount",
        ]
        read_only_fields = [
            "customer",
            "coupon",
            "total_price",
            "created_at",
            "updated_at",
        ]
