from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    images = models.JSONField(default=list)  # product photos
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
