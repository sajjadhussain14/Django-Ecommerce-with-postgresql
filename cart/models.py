from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from ecommerce.models import Products
from django.contrib.auth.models import User  # You may need to import your custom user model if you're using one

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Products, through='WishlistItem')

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    attributes = models.JSONField()  # Store product attributes as JSON data

    class Meta:
        unique_together = ('wishlist', 'product')
