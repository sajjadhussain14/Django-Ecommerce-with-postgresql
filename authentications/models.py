# authentications/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    billing_first_name = models.CharField(max_length=255, blank=True)
    billing_last_name = models.CharField(max_length=255, blank=True)
    
    billing_address_line1 = models.CharField(max_length=255, blank=True)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=255, blank=True)
    billing_state = models.CharField(max_length=255, blank=True)
    billing_country = models.CharField(max_length=255, blank=True)
    billing_phone = models.CharField(max_length=15, blank=True)

    shipping_first_name = models.CharField(max_length=255, blank=True)
    shipping_last_name = models.CharField(max_length=255, blank=True)
    shipping_address_line1 = models.CharField(max_length=255, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=255, blank=True)
    shipping_state = models.CharField(max_length=255, blank=True)
    shipping_country = models.CharField(max_length=255, blank=True)
    shipping_phone = models.CharField(max_length=15, blank=True)

    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    # Add any other custom fields you need

    # Set the email as the unique identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
