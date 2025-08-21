class Payment(models.Model):
    order = models.OneToOneField("Order", on_delete=models.CASCADE, related_name="payment")
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[("card", "Card"), ("upi", "UPI"), ("cod", "Cash on Delivery")])
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("success", "Success"), ("failed", "Failed")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"
