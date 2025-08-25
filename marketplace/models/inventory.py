from django.db import models
from accounts.models import Company
from .product import Product

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventories")  
    stock_quantity = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_flash_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'company')  # same product can’t be listed twice by same company

    def __str__(self):
        return f"{self.product.name} by {self.company.name}"
