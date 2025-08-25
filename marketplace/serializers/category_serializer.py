from rest_framework import serializers
from marketplace.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "parent", "subcategories"]

    def get_subcategories(self, obj):
        # Fetch subcategories of this category
        subcats = ProductCategory.objects.filter(parent=obj)
        return ProductCategorySerializer(subcats, many=True).data
