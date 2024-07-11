from django.contrib.auth import get_user_model
from django.db import models
from shop.models import Product


class OrderStatus(models.TextChoices):
    STATUS_PENDING = "Pending"
    STATUS_PAID = "Paid"
    STATUS_CANCELLED = "Cancelled"
    STATUS_REFUNDED = "Refunded"
    STATUS_SHIPPED = "Shipped"
    STATUS_DELIVERED = "Delivered"
    STATUS_COMPLETED = "Completed"


class Order(models.Model):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, null=True, blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.STATUS_PENDING
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
