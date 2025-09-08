from .models import Cart, CartItem

def merge_guest_cart(user, request):
    """
    Merge guest session cart with user's cart after login.
    """
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        guest_cart = Cart.objects.get(session_key=session_key, buyer=None)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(buyer=user)

    # Merge items
    for item in guest_cart.items.all():
        existing_item, created = CartItem.objects.get_or_create(
            cart=user_cart, inventory=item.inventory,
            defaults={"quantity": item.quantity}
        )
        if not created:
            existing_item.quantity += item.quantity
            existing_item.save()

    # Delete guest cart
    guest_cart.delete()

    # Update session cart_id to point to user cart
    request.session["cart_id"] = user_cart.id
