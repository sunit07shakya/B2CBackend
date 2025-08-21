from django.db import models, transaction
from accounts.models import CustomUser
from .inventory import Inventory


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address_snapshot = models.TextField()  # snapshot of address at time of order
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # seller-specific listing
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)  # locked price

    def __str__(self):
        return f"{self.quantity} x {self.inventory.product.name} (Seller: {self.inventory.company.name})"

    def save(self, *args, **kwargs):
        """
        Override save() to automatically reduce stock from inventory when new order item is created.
        """
        if not self.pk:  # only on first creation (not update)
            with transaction.atomic():
                inventory = Inventory.objects.select_for_update().get(pk=self.inventory.pk)

                if inventory.stock_quantity < self.quantity:
                    raise ValueError(f"Not enough stock for {inventory.product.name} (Seller: {inventory.company.name})")

                # Deduct stock
                inventory.stock_quantity -= self.quantity
                inventory.save()

        super().save(*args, **kwargs)
