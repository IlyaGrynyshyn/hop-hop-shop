from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from shop.models import Product, Category, ProductAttributes
from cart.models import Cart, CartItem


class CartTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )

        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

        self.product1 = Product.objects.create(
            name="Test Product 1",
            category=self.category,
            slug="test-product-1",
            price=10,
            SKU=111,
            description="Test Product 1 Description",
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            category=self.category,
            slug="test-product-2",
            price=20,
            SKU=222,
            description="Test Product 2 Description",
        )

        self.product1_attributes = ProductAttributes.objects.create(
            product=self.product1,
            brand="Brand 1",
            material="Material 1",
            style="Style 1",
            size=1,
        )

        self.product2_attributes = ProductAttributes.objects.create(
            product=self.product2,
            brand="Brand 2",
            material="Material 2",
            style="Style 2",
            size=2,
        )

        self.client = Client()

    def test_add_to_cart(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product1)
        self.assertEqual(cart.items.first().quantity, 1)

    def test_view_cart(self):
        self.client.login(username="testuser", password="testpass")
        self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        response = self.client.get(reverse("cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "10")

    def test_update_cart(self):
        self.client.login(username="testuser", password="testpass")
        self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product1)
        response = self.client.patch(
            reverse("update_cart", args=[cart_item.id]),
            {"quantity": 5},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_remove_from_cart(self):
        self.client.login(username="testuser", password="testpass")
        self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product1)
        response = self.client.post(reverse("remove_from_cart", args=[cart_item.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)
