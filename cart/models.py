from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.email}"
        return f"Cart with session {self.session_key}"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"

    def item_total_price(self):
        return self.product.price * self.quantity
