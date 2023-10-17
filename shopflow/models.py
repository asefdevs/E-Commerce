from django.db import models

from accounts.models import CustomUser
from estore.models import Product


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='cartitem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'cart for {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    is_ordered=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.cart}'


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_favrorites')

    def __str__(self):
        return f'{self.product} for {self.user.username}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('bank_card', 'Bank Card'),
        ('cash', 'Cash'),
    )

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_order')
    products=models.ManyToManyField(CartItem,related_name='orders',blank=True)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled=models.BooleanField(default=False)

    def __str__(self):
        return f'Order for {self.cart.user.username}'

    def save(self, *args, **kwargs):
        total = sum(item.product.price *
                    item.quantity for item in self.cart.cart_items.all())
        self.total_amount = total
        super(Order, self).save(*args, **kwargs)
