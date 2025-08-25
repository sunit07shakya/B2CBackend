# your_app/views/product_views.py
from rest_framework import generics, filters
from marketplace.models.product import Product,ProductCategory
from marketplace.serializers.product_serializer import ProductSerializer,ProductCategorySerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "category__name"]

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related("inventories__company", "category")

        # 🔍 Name search (already handled by SearchFilter, but can add fallback)
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 💰 Price filter (from inventories)
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if min_price and max_price:
            queryset = queryset.filter(inventories__selling_price__gte=min_price, inventories__selling_price__lte=max_price)
        elif min_price:
            queryset = queryset.filter(inventories__selling_price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(inventories__selling_price__lte=max_price)

        # 🏷 Category filter
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__id=category)

        # 🌍 City filter (from company model)
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(inventories__company__city__icontains=city)

        return queryset.distinct()

class CategoryListView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().prefetch_related("inventories")
    serializer_class = ProductSerializer