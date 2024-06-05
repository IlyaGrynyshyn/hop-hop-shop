from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Product
from cart.models import Cart, CartItem


class CartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(name="Test Product", price=100.0)
        self.client.login(username="testuser", password="12345")

    def test_cart_view(self):
        response = self.client.get(reverse("cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart_detail.html")

    def test_add_to_cart(self):
        response = self.client.post(reverse("add_to_cart", args=[self.product.id]))
        self.assertRedirects(response, reverse("cart_detail"))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)

    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse("remove_from_cart", args=[cart_item.id]))
        self.assertRedirects(response, reverse("cart_detail"))
        self.assertEqual(cart.items.count(), 0)
