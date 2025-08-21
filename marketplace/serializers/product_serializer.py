from rest_framework import serializers
from marketplace.models.product import Product, ProductCategory
from marketplace.models.inventory import Inventory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "images", "created_at"]


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "company",
            "stock_quantity",
            "selling_price",
            "min_selling_price",
            "max_selling_price",
            "is_available",
            "created_at"
        ]
