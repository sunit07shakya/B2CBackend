from rest_framework import serializers
from marketplace.models import Inventory
from marketplace.serializers.company_serializer import CompanySerializer

class InventorySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "company",
            "stock_quantity",
            "selling_price",
            "min_selling_price",
            "max_selling_price",
            "is_available",
            "created_at",
        ]
