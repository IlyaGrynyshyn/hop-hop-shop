from rest_framework import serializers
from .models import Category, Product, ProductAttributes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ['id', 'brand', 'material', 'style', 'size', 'product']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'SKU', 'description', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes = ProductAttributesSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'SKU', 'description', 'category', 'attributes']