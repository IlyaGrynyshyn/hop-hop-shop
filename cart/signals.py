from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.models import Cart


@receiver(user_logged_in)
def merge_session_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    try:
        session_cart = Cart.objects.get(session_key=session_key)
        user_cart, created = Cart.objects.get_or_create(user=user)
        user_cart.merge_with(session_cart)
    except Cart.DoesNotExist:
        pass
