# shop/cart/tests/test_serializers.py

from django.test import TestCase
from shop.models import Category, Product, ProductAttributes
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ProductAttributesSerializer,
)


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_category_serialization(self):
        serializer = CategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["id", "name", "slug"]))
        self.assertEqual(data["name"], "Test Category")
        self.assertEqual(data["slug"], "test-category")


class ProductAttributesSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            SKU="SKU123",
            description="Description",
            category=self.category,
        )
        self.attributes = ProductAttributes.objects.create(
            brand="Test Brand",
            material="Test Material",
            style="Test Style",
            size="Test Size",
            product=self.product,
        )

    def test_product_attributes_serialization(self):
        serializer = ProductAttributesSerializer(self.attributes)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "brand", "material", "style", "size", "product"]),
        )
        self.assertEqual(data["brand"], "Test Brand")
        self.assertEqual(data["material"], "Test Material")
        self.assertEqual(data["style"], "Test Style")
        self.assertEqual(data["size"], "Test Size")
        self.assertEqual(data["product"], self.product.id)


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            SKU="SKU123",
            description="Description",
            category=self.category,
        )

    def test_product_serialization(self):
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "name", "slug", "price", "SKU", "description", "category"]),
        )
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["slug"], self.product.slug)
        self.assertEqual(
            data["price"], "100.00"
        )  # Django REST framework returns Decimal as string
        self.assertEqual(data["SKU"], "SKU123")
        self.assertEqual(data["description"], "Description")
        self.assertEqual(data["category"], self.category.id)


class ProductDetailSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            SKU="SKU123",
            description="Description",
            category=self.category,
        )
        self.attributes = ProductAttributes.objects.create(
            brand="Test Brand",
            material="Test Material",
            style="Test Style",
            size="Test Size",
            product=self.product,
        )

    def test_product_detail_serialization(self):
        serializer = ProductDetailSerializer(self.product)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "slug",
                    "price",
                    "SKU",
                    "description",
                    "category",
                    "attributes",
                ]
            ),
        )
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["slug"], self.product.slug)
        self.assertEqual(data["price"], "100.00")
        self.assertEqual(data["SKU"], "SKU123")
        self.assertEqual(data["description"], "Description")
        self.assertEqual(data["category"]["id"], self.category.id)
        self.assertEqual(data["attributes"]["brand"], "Test Brand")
        self.assertEqual(data["attributes"]["material"], "Test Material")
        self.assertEqual(data["attributes"]["style"], "Test Style")
        self.assertEqual(data["attributes"]["size"], "Test Size")
        self.assertEqual(data["attributes"]["product"], self.product.id)
