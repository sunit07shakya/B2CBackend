# marketplace/views/landing.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from ..models import Product
from ..serializers.product_serializer import ProductSerializer

class LandingAPI(APIView):
    """
    Landing API → Top 10 products, featured, flash sale, recently viewed
    """

    def get(self, request):
        # 1. Top products (let’s assume based on number of inventories or avg rating later)
        top_products = Product.objects.annotate(
            num_inventories=Count("inventories")
        ).order_by("-num_inventories")[:10]

        
        # 2. Featured products → products having at least one featured inventory
        featured_products = Product.objects.filter(
            inventories__is_featured=True
        ).distinct()[:10]

        # 3. Flash sale products → products having at least one flash sale inventory
        flash_sale_products = Product.objects.filter(
            inventories__is_flash_sale=True
        ).distinct()[:10]

        # 4. Recently viewed
        if request.user.is_authenticated:
            recent_ids = list(request.user.recent_views.values_list("product_id", flat=True)[:10])
        else:
            recent_ids = request.session.get("recent_viewed", [])[:10]

        recent_products = Product.objects.filter(id__in=recent_ids)
        # preserve order based on `recent_ids`
        recent_products_dict = {p.id: p for p in recent_products}
        recent_products = [recent_products_dict[pid] for pid in recent_ids if pid in recent_products_dict]

        return Response({
            "top_products": ProductSerializer(top_products, many=True).data,
            "featured_products": ProductSerializer(featured_products, many=True).data,
            "flash_sale": ProductSerializer(flash_sale_products, many=True).data,
            "recent_viewed": ProductSerializer(recent_products, many=True).data,
        }, status=status.HTTP_200_OK)
