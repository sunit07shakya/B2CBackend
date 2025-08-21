# your_app/views/product_views.py
from rest_framework import generics
from marketplace.models.product import Product,ProductCategory
from marketplace.serializers.product_serializer import ProductSerializer,ProductCategorySerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
