from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from datetime import date
import random
from django.utils.crypto import get_random_string
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# create Categories Table
class Categories(MPTTModel):
    name = models.CharField(max_length=255, db_index=True)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    slug = models.SlugField(max_length=255, unique=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_page", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "1. Categories"


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "2. Attributes"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    color_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "3. Attribute Values"

    def __str__(self):
        return self.value


class Brands(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="brand_images", blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Products(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, blank=True)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    attributes = models.ManyToManyField(Attribute, through="ProductAttribute")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "4. Products"

    def __str__(self):
        return self.title


class Images(models.Model):
    product = models.ForeignKey(
        Products, default=None, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="prod_images", blank=True, default="default.jpg"
    )

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.attribute}: {self.value}"


class Variation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Sku = models.CharField(
        max_length=255, blank=True, editable=True, unique=True, default=uuid.uuid4
    )
    stock = models.PositiveIntegerField()
    attributes = models.ManyToManyField(Attribute, through="VariationAttribute")
    # Add this field for the image
    image = models.ImageField(upload_to="variation_Images/", blank=True, null=True)

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "5. Product Variations"

    def __str__(self):
        return self.Sku


class VariationAttribute(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variation} - {self.attribute}: {self.value}"


import uuid
from django.db import models


class MainBanner(models.Model):
    name = models.CharField(max_length=255)
    content_id = models.UUIDField(default=uuid.uuid4, editable=True)
    text1 = models.TextField(blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)
    text3 = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="main_banners/")
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    is_active = models.BooleanField(
        default=True, editable=True
    )  # Renamed to "is_active"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(MainBanner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MainBanner"
        verbose_name_plural = "1. MainBanners"


class MiniBanner(models.Model):
    name = models.CharField(max_length=255)
    content_id = models.UUIDField(default=uuid.uuid4, editable=True)
    text1 = models.TextField(blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)
    text3 = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="main_banners/")
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    is_active = models.BooleanField(
        default=True, editable=True
    )  # Renamed to "is_active"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(MiniBanner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MiniBanner"
        verbose_name_plural = "1. MiniBanners"


class Logo(models.Model):
    image = models.ImageField(
        upload_to="logo_images", blank=True, null=True, default="default_logo.png"
    )
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "1. Logo"


@receiver(post_save, sender=Logo)
def ensure_single_logo(sender, instance, **kwargs):
    if kwargs.get("created", False):
        # Delete any additional Logo instances
        Logo.objects.exclude(pk=instance.pk).delete()
