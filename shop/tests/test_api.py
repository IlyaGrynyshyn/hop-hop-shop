from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Category, Product
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
)
from django.urls import reverse


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.category_url = reverse("category-list")

    def test_list_categories(self):
        response = self.client.get(self.category_url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_category(self):
        url = reverse("category-detail", args=[self.category.id])
        response = self.client.get(url)
        serializer = CategorySerializer(self.category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            category=self.category,
            SKU=1231,
            views=0,
        )
        self.product_url = reverse("product-list")
        self.detail_url = reverse("product-detail", args=[self.product.id])

    def test_list_products(self):
        response = self.client.get(self.product_url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        self.product.refresh_from_db()
        serializer = ProductDetailSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.product.views, 1)

    def test_popular_products(self):
        popular_url = reverse("product-popular")
        response = self.client.get(popular_url)
        popular_products = Product.objects.order_by("-views")[:30]
        serializer = ProductSerializer(popular_products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
