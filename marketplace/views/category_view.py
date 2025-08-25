from rest_framework import generics
from marketplace.models import ProductCategory
from marketplace.serializers.category_serializer import ProductCategorySerializer

# List + Create categories
class ProductCategoryListCreateView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.filter(parent__isnull=True)  
    serializer_class = ProductCategorySerializer


# Retrieve + Update + Delete specific category
class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
