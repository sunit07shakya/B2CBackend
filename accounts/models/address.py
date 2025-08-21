from django.db import models
from django.conf import settings


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="addresses",
        blank=True,
        null=True
    )
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)  # extra for delivery
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    address_type = models.CharField(
        max_length=20,
        choices=[
            ("home", "Home"),
            ("work", "Work"),
            ("billing", "Billing"),
            ("shipping", "Shipping"),
            ("office", "Office"),
            ("warehouse", "Warehouse"),
        ],
        default="home"
    )
    is_default = models.BooleanField(default=False)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        owner = self.user.username if self.user else (self.company.name if self.company else "Unknown")
        return f"{self.address_line1}, {self.city} ({owner})"
