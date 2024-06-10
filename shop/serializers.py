from rest_framework import serializers
from shop.models import Category, Product, ProductAttributes, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ["id", "brand", "material", "style", "size", "product"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    product_image = ProductImageSerializer(
        many=True, read_only=True, source="product_images"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "SKU",
            "description",
            "category",
            "product_image",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes = ProductAttributesSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "SKU",
            "description",
            "category",
            "attributes",
            "product_image",
        ]
