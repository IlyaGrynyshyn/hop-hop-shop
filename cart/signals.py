from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from cart.models import Cart
import json


@receiver(user_logged_in)
def merge_session_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if not session_key:
        return
    try:
        session_cart = Cart.objects.get(session_key=session_key)
        user_cart, created = Cart.objects.get_or_create(user=user)
        if session_cart != user_cart:
            user_cart.merge_with(session_cart)
    except Cart.DoesNotExist:
        pass


@receiver(user_logged_out)
def save_cart_on_logout(sender, request, user, **kwargs):
    try:
        user_cart = Cart.objects.get(user=user)
        cart_data = {
            str(item.product.id): item.quantity for item in user_cart.items.all()
        }
        user_cart.old_cart = json.dumps(cart_data)
        user_cart.save()
    except Cart.DoesNotExist:
        pass
