from rest_framework import serializers
from shop.models import Product
from shop.serializers import ProductSerializer


class CustomProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "image", "category", "slug"]
