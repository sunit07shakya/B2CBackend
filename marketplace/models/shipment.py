class Shipment(models.Model):
    order = models.OneToOneField("Order", on_delete=models.CASCADE, related_name="shipment")
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
