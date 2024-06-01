from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Product
from shop.serializers import ProductSerializer


class PopularProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product1 = Product.objects.create(name="Product 1", views=50)
        self.product2 = Product.objects.create(name="Product 2", views=300)
        self.product3 = Product.objects.create(name="Product 3", views=150)
        self.product4 = Product.objects.create(name="Product 4", views=75)

        self.url = "/products/popular/"

    def test_retrieve_popular_products(self):
        response = self.client.get(self.url)
        products = Product.objects.order_by("-views")[:30]
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_popular_products_order(self):
        response = self.client.get(self.url)
        views = [product["views"] for product in response.data]

        self.assertEqual(views, sorted(views, reverse=True))

    def test_popular_products_limit(self):
        response = self.client.get(self.url)

        self.assertLessEqual(len(response.data), 30)
