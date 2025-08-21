from django.contrib import admin
from .models import (
    Product, ProductCategory,
    Review,
    Cart, CartItem,
    Order, OrderItem,
    Inventory
)

# -----------------------------
# Product Category
# -----------------------------
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)


# -----------------------------
# Product
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 
        'created_at'
    )
    # list_filter = ( 'category')
    # search_fields = ('name')


# -----------------------------
# Review
# -----------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'buyer__username')


# -----------------------------
# Cart & Cart Items
# -----------------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'created_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'quantity')
    list_filter = ('id',)


# -----------------------------
# Orders & Order Items
# -----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'id')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'quantity', 'price_at_purchase')
    list_filter = ('order',)


# -----------------------------
# Inventory
# -----------------------------
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'stock_quantity', )
    list_filter = ('product',)
