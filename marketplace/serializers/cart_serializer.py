from rest_framework import serializers
from ..models import Cart, CartItem, Inventory, Product


class CartProductSerializer(serializers.ModelSerializer):
    """Custom product data inside cart"""

    class Meta:
        model = Product
        fields = ["id", "name", "description", "created_at"]  # 👈 only selected fields


class CartInventorySerializer(serializers.ModelSerializer):
    """Inventory + partial product"""
    product = CartProductSerializer(read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Inventory
        fields = ["id", "selling_price", "stock_quantity", "is_available", "product", "company_name"]


class CartItemSerializer(serializers.ModelSerializer):
    inventory = CartInventorySerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "inventory", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "buyer", "items", "created_at"]
