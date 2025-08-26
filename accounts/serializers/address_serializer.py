from rest_framework import serializers
from accounts.models.address import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_line1",
            "address_line2",
            "landmark",
            "city",
            "state",
            "country",
            "postal_code",
            "address_type",
            "is_default",
            "latitude",
            "longitude",
        ]
