from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Product
from cart.models import Cart, CartItem


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.cart = Cart.objects.create(user=self.user)
        self.product1 = Product.objects.create(name="Product 1", price=100.0)
        self.product2 = Product.objects.create(name="Product 2", price=200.0)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, "testuser")

    def test_total_price(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        self.assertEqual(self.cart.total_price(), 500.0)

    def test_item_count(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        self.assertEqual(self.cart.item_count(), 3)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(name="Test Product", price=100.0)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart.user.username, "testuser")
        self.assertEqual(self.cart_item.product.name, "Test Product")
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.item_total_price(), 200.0)
