from django.db import models
from accounts.models import CustomUser
from .inventory import Inventory

class Cart(models.Model):
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="cart", blank=True, null=True
    )
    session_key = models.CharField(max_length=100, blank=True, null=True,db_index=True)  # guest tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.buyer:
            return f"Cart #{self.id} for {self.buyer.username}"
        return f"Guest Cart (session: {self.session_key})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # 🔥 seller-specific listing
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.inventory.product.name} ({self.inventory.company.name})"
