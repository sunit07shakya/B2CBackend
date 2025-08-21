from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)  # e.g., +91
    alternate_email = models.EmailField(blank=True, null=True)

    # Account settings
    is_verified = models.BooleanField(default=False)   # email/phone verification
    kyc_verified = models.BooleanField(default=False)  # for sellers

    # Tracking
    signup_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
