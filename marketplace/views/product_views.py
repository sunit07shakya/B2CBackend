# your_app/views/product_views.py
from rest_framework import generics, filters
from marketplace.models.product import Product,ProductCategory
from marketplace.serializers.product_serializer import ProductSerializer,ProductCategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related("inventories__company", "category")
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "category__name"]

class CategoryListView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().prefetch_related("inventories")
    serializer_class = ProductSerializer