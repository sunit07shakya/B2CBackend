from django.db import models
from accounts.models import CustomUser
from .product import Product


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # ⭐ 1–5 rating

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    buyer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "buyer")  # ✅ Prevent multiple reviews from same buyer
        ordering = ["-created_at"]  # latest reviews first

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐ by {self.buyer.username}"

    @property
    def short_comment(self):
        """Truncate long comments for preview use cases"""
        return (self.comment[:50] + "...") if self.comment and len(self.comment) > 50 else self.comment
