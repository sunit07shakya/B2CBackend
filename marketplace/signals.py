# marketplace/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem


@receiver(user_logged_in)
def merge_guest_cart(sender, user, request, **kwargs):
    """
    When a guest logs in, merge their session cart into user cart.
    """
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        guest_cart = Cart.objects.get(session_key=session_key, buyer=None)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create_cart(buyer=user)

    # Merge items
    for item in guest_cart.items.all():
        existing_item, created = CartItem.objects.get_or_create_cart(
            cart=user_cart, inventory=item.inventory
        )
        if not created:
            existing_item.quantity += item.quantity
            existing_item.save()
        else:
            existing_item.quantity = item.quantity
            existing_item.save()

    # Delete guest cart after merge
    guest_cart.delete()
