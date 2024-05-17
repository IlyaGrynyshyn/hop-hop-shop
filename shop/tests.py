from django.test import TestCase
from .models import Category, Product, ProductImage, ProductAttributes

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_unique(self):
        category = Category.objects.create(name='Test Category')
        category_duplicate = Category(name='Test Category')
        with self.assertRaises(Exception):
            category_duplicate.full_clean()

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(expected_object_name, str(category))

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        Product.objects.create(name='Test Product', category=category, price=100, SKU=12345, description='Test description')

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

class ProductImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(name='Test Product', category=category, price=100, SKU=12345, description='Test description')
        ProductImage.objects.create(product=product, image='test_image.jpg')

    def test_image_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

class ProductAttributesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(name='Test Product', category=category, price=100, SKU=12345, description='Test description')
        ProductAttributes.objects.create(brand='Test Brand', material='Test Material', style='Test Style', size='Test Size', product=product)

    def test_brand_label(self):
        product_attributes = ProductAttributes.objects.get(id=1)
        field_label = product_attributes._meta.get_field('brand').verbose_name
        self.assertEqual(field_label, 'brand')