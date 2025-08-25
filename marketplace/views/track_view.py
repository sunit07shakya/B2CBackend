# marketplace/views/landing.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from ..models import Product

class TrackViewAPI(APIView):
    """
    Track product views for guest (session) or logged-in user.
    """

    def post(self, request, product_id):
        if request.user.is_authenticated:
            # If logged in → Save in DB (optional RecentView model)
            recent = request.user.recent_views.values_list("product_id", flat=True)
            if product_id in recent:
                request.user.recent_views.filter(product_id=product_id).delete()
            request.user.recent_views.create(product_id=product_id)

        else:
            # If guest → save in session
            recent = request.session.get("recent_viewed", [])
            if product_id in recent:
                recent.remove(product_id)
            recent.insert(0, product_id)
            request.session["recent_viewed"] = recent[:20]  # keep last 20
            request.session.modified = True

        return Response({"message": "Tracked successfully"}, status=status.HTTP_200_OK)

