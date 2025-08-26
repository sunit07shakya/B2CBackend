from rest_framework import serializers
from accounts.models import Company
from accounts.serializers.address_serializer import AddressSerializer

class CompanySerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = ["id", "name", "description","addresses", "website", "is_verified"]
