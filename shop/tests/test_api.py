from django.core.files.uploadedfile import SimpleUploadedFile
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

        self.image1 = SimpleUploadedFile(
            name="test_image1.jpg", content=b"\x00\x01", content_type="image/jpeg"
        )
        self.image2 = SimpleUploadedFile(
            name="test_image2.jpg", content=b"\x00\x02", content_type="image/jpeg"
        )

    def test_create_product_invalid_category(self):
        data = {
            "name": "Test Product 2",
            "category": 999,
            "price": 100,
            "SKU": 3333,
            "description": "Test Description",
        }
        response = self.client.post(self.product_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product(self):
        data = {
            "name": "Test Product 2",
            "category": self.category.id,
            "price": 100,
            "SKU": 3333,
            "description": "Test Description",
            "product_attributes": {
                "brand": "Test Brand",
                "material": "Test Material",
                "style": "Test Style",
                "size": 42,
            },
        }

        response = self.client.post(self.product_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.get(id=response.data["id"])
        self.assertEqual(product.name, "Test Product 2")
        self.assertEqual(product.category.id, self.category.id)
        self.assertEqual(product.price, 100)
        self.assertEqual(product.SKU, 3333)
        self.assertEqual(product.description, "Test Description")
        #
        # image1 = SimpleUploadedFile(
        #     name="test_image1.jpg", content=b"\x00\x01", content_type="image/jpeg"
        # )
        # image2 = SimpleUploadedFile(
        #     name="test_image2.jpg", content=b"\x00\x02", content_type="image/jpeg"
        # )
        #
        # image_upload_url = reverse("product-upload-images", args=[product.id])
        # image_data = {"uploaded_images": [image1, image2]}
        #
        # response = self.client.post(image_upload_url, image_data, format="multipart")
        #
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_upload_images(self):
    #     url = reverse("product-upload-images", args=[self.product.id])
    #     image1 = SimpleUploadedFile(
    #         name="test_image1.jpg", content=b"\x00\x01", content_type="image/jpeg"
    #     )
    #     image2 = SimpleUploadedFile(
    #         name="test_image2.jpg", content=b"\x00\x02", content_type="image/jpeg"
    #     )
    #
    #     image_upload_url = reverse("product-upload-images", args=[self.product.id])
    #     image_data = {"uploaded_images": [image1, image2]}
    #
    #     response = self.client.post(image_upload_url, image_data, format="multipart")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_product(self):
        update_data = {
            "name": "Partially Updated Product",
        }
        response = self.client.patch(self.detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, update_data["name"])

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

    def test_update_product(self):
        update_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 150.00,
            "SKU": 12345,
            "category": self.category.id,
            "product_attributes": {
                "brand": "Updated Brand",
                "material": "Updated Material",
                "style": "Updated Style",
                "size": 42,
            },
        }
        response = self.client.patch(self.detail_url, update_data, format="json")
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.name, update_data["name"])
        self.assertEqual(self.product.description, update_data["description"])
        self.assertEqual(self.product.price, update_data["price"])
