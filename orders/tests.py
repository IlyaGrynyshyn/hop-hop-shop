from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from shop.models import Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product1 = Product.objects.create(
            name="Test Product 1", price=10, stock=100
        )
        self.product2 = Product.objects.create(
            name="Test Product 2", price=20, stock=50
        )

        self.client = Client()

    def test_checkout(self):
        self.client.login(username="testuser", password="testpass")
        self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], "Order placed")
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        self.assertEqual(OrderItem.objects.filter(order__user=self.user).count(), 1)
        self.assertEqual(Product.objects.get(id=self.product1.id).stock, 99)

    def test_insufficient_stock_checkout(self):
        self.client.login(username="testuser", password="testpass")
        self.client.post(reverse("add_to_cart", args=[self.product2.id]))
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product2)
        cart_item.quantity = 51
        cart_item.save()
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], f"Not enough stock for {self.product2.name}"
        )
