from cart.models import Cart, CartItem


class CartTransferMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                session_cart = Cart.objects.filter(session_key=session_key).first()
                if session_cart:
                    user_cart, created = Cart.objects.get_or_create(user=request.user)
                    for item in session_cart.items.all():
                        print(item)
                        user_cart_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={"quantity": item.quantity},
                        )
                        if not created:
                            user_cart_item.quantity += item.quantity
                            user_cart_item.save()
                    session_cart.delete()

        return response
