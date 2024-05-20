import os
import uuid

from django.db import models
from pytils.translit import slugify


def product_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.product.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/products/", filename)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.IntegerField()
    SKU = models.IntegerField(unique=True, db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["id"]


class ProductImage(models.Model):
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_image_file_path,
        max_length=255,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        ordering = ["id"]


class ProductAttributes(models.Model):
    brand = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    size = models.IntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attributes for {self.product.name}"
