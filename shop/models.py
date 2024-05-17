from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    SKU = models.IntegerField(unique=True, db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductAttributes(models.Model):
    brand = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    size = models.IntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attributes for {self.product.name}"
