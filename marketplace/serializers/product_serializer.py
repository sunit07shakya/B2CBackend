from rest_framework import serializers
from marketplace.models.product import Product, ProductCategory
from marketplace.models.inventory import Inventory
from marketplace.serializers.company_serializer import CompanySerializer
from marketplace.serializers.inventory_serializer import InventorySerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    inventories = InventorySerializer(many=True, read_only=True) 

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category","inventories", "images", "created_at"]


