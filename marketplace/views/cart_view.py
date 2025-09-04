# marketplace/views/cart.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart, CartItem, Inventory
from ..serializers.cart_serializer import CartSerializer


def get_or_create_cart(request):
    """Get or create cart for logged-in user or guest (session-based)."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(buyer=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(buyer=None, session_key=request.session.session_key)
    return cart


class CartView(APIView):
    """Fetch cart (user or guest)"""

    def get(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(buyer=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToCartView(APIView):
    """Add a product (inventory) to cart"""

    def post(self, request):
        inventory_id = request.data.get("inventory_id")
        quantity = int(request.data.get("quantity", 1))

        cart = get_or_create_cart(request)

        try:
            inventory = Inventory.objects.get(id=inventory_id)
        except Inventory.DoesNotExist:
            return Response({"error": "Invalid inventory_id"}, status=status.HTTP_400_BAD_REQUEST)

          # 🔒 Stock check
        if quantity > inventory.stock_quantity:
            return Response(
                {"error": f"Only {inventory.stock_quantity} units available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if item already exists in cart
        item, created = CartItem.objects.get_or_create(cart=cart, inventory=inventory)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

class UpdateCartItemView(APIView):
    def post(self, request):
        inventory_id = request.data.get("inventory_id")
        quantity = int(request.data.get("quantity", 1))
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(inventory_id=inventory_id, cart=cart)
             # 🔒 Stock check
            if quantity > item.inventory.stock_quantity:
                return Response(
                    {"error": f"Only {item.inventory.stock_quantity} units available"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.quantity = quantity
            item.save()
        except CartItem.DoesNotExist:
            return Response({"error": "Invalid inventory_id"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CartSerializer(cart).data)


class RemoveCartItemView(APIView):
    """Remove item from cart"""

    def post(self, request):
        inventory_id = request.data.get("inventory_id")

        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(cart=cart, inventory_id=inventory_id)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({"error": "Invalid inventory_id"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CartSerializer(cart).data)
