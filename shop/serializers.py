from rest_framework import serializers
from shop.models import Category, Product, ProductAttributes, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image"]


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ["brand", "material", "style", "size"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source="product_images")
    product_attributes = ProductAttributesSerializer(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "slug",
            "price",
            "SKU",
            "description",
            "views",
            "images",
            "product_attributes",
        ]
        read_only_fields = ["slug", "views"]

    def create(self, validated_data):
        product_attributes_data = validated_data.pop("product_attributes", None)
        product = Product.objects.create(**validated_data)
        if product_attributes_data:
            product_attributes_data["product"] = product
            ProductAttributes.objects.create(**product_attributes_data)

        return product


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
