from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(blank=True, null=True)
    size = models.CharField(max_length=80, blank=True, null=True)
    color = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(
        default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
