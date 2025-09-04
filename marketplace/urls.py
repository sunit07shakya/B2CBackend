from django.urls import path
from marketplace.views import ProductListView,ProductDetailView
from .views.landing_view import LandingAPI
from .views.track_view import TrackViewAPI
from .views.cart_view import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

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

    # Cart URLs
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/update/", UpdateCartItemView.as_view(), name="update_cart_item"),
    path("cart/remove/", RemoveCartItemView.as_view(), name="remove_cart_item"),
]
