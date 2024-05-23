import os
import uuid

from django.db.utils import IntegrityError
from django.test import TestCase
from factory import Factory, Faker, SubFactory

from shop.models import (
    Category,
    Product,
    ProductImage,
    ProductAttributes,
    product_image_file_path,
)


class CategoryFactory(Factory):
    class Meta:
        model = Category

    name = Faker("word")


class ProductFactory(Factory):
    class Meta:
        model = Product

    name = Faker("word")
    category = SubFactory(CategoryFactory)
    price = Faker("random_number", digits=5)
    SKU = Faker("random_number", digits=10)
    description = Faker("text")


class ProductImageFactory(Factory):
    class Meta:
        model = ProductImage

    product = SubFactory(ProductFactory)
    image = None


class ProductAttributesFactory(Factory):
    class Meta:
        model = ProductAttributes

    brand = Faker("word")
    material = Faker("word")
    style = Faker("word")
    size = Faker("random_number", digits=2)
    product = SubFactory(ProductFactory)


class CategoryModelTest(TestCase):

    def test_string_representation(self):
        category = CategoryFactory(name="Test Category")
        category.save()
        self.assertEqual(str(category), category.name)

    def test_slug_generation_on_save(self):
        category = CategoryFactory(name="Test Category")
        category.save()
        self.assertEqual(category.slug, "test-category")


class ProductModelTest(TestCase):

    def test_string_representation(self):
        product = ProductFactory(name="Test Product")
        product.category.save()
        product.save()
        self.assertEqual(str(product), product.name)

    def test_slug_generation_on_save(self):
        product = ProductFactory(name="Test Product")
        product.category.save()
        product.save()
        self.assertEqual(product.slug, "test-product")

    def test_unique_sku(self):
        product = ProductFactory.create(SKU=1234567890)
        product.category.save()
        product.save()

        with self.assertRaises(IntegrityError):
            duplicate_product = ProductFactory.build(SKU=1234567890)
            duplicate_product.category.save()
            duplicate_product.save()


class ProductImageModelTest(TestCase):

    def test_string_representation(self):
        product_image = ProductImageFactory()
        self.assertEqual(str(product_image), f"Image for {product_image.product.name}")

    def test_image_upload_path(self):
        product_image = ProductImageFactory()
        product_image.product.name = "Test Product"
        filename = "example.jpg"
        path = product_image_file_path(product_image, filename)
        expected_path = os.path.join(
            "uploads/products/", f"test-product-{uuid.uuid4()}.jpg"
        )
        self.assertTrue(path.startswith("uploads/products/test-product-"))
        self.assertTrue(path.endswith(".jpg"))


class ProductAttributesModelTest(TestCase):

    def test_string_representation(self):
        product_attributes = ProductAttributesFactory()
        self.assertEqual(
            str(product_attributes), f"Attributes for {product_attributes.product.name}"
        )
