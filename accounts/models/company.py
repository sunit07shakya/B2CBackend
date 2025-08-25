from django.db import models
from django.conf import settings


class Company(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    # Compliance / Business details
    gst_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True, unique=True)

    # Optional business fields
    industry_type = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Textiles"
    employee_count = models.IntegerField(blank=True, null=True)
    annual_turnover = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # INR/USD
    is_verified = models.BooleanField(default=False)  # Admin approval / KYC flag

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
