from django.urls import path
from marketplace.views import ProductListView,ProductDetailView
from .views.landing_view import LandingAPI
from .views.track_view import TrackViewAPI

from marketplace.views.category_view import (
    ProductCategoryListCreateView,
    ProductCategoryDetailView,
)
urlpatterns = [
    # Landing page
    path("landing/", LandingAPI.as_view(), name="landing"),
    path("products/<int:product_id>/track-view/", TrackViewAPI.as_view(), name="track-view"),

    # Product URLs
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    
    # Category URLs
    path("categories/", ProductCategoryListCreateView.as_view(), name="category-list"),
    path("categories/<int:pk>/", ProductCategoryDetailView.as_view(), name="category-detail"),
]
