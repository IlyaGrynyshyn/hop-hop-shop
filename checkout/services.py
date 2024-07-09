import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from cart.services import CartSessionService
from checkout.models import Order, OrderItem
from shop.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_order(validated_data, request):
    card_information = validated_data.pop("card_information", None)
    cart = CartSessionService(request)

    items_data = [
        {
            "product": Product.objects.get(id=item["product"]["id"]),
            "quantity": item["quantity"],
            "price": item["price"],
        }
        for item in cart
    ]

    order = Order.objects.create(**validated_data)
    for item_data in items_data:
        OrderItem.objects.create(order=order, **item_data)
    cart.clear()
    return order, card_information, cart.get_total_price()


def stripe_card_payment(card_information: dict, total_price: float):
    payment_method_data = {
        "type": "card",
        "card": {
            "number": card_information["card_number"],
            "exp_month": card_information["expiry_month"],
            "exp_year": card_information["expiry_year"],
            "cvc": card_information["cvc"],
        },
    }
    try:
        stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency="usd",
            payment_method_data=payment_method_data,
            confirm=True,
            return_url="http://127.0.0.1:8000/api/doc/",
        )
        response = {"message": "Card Payment Success", "status": status.HTTP_200_OK}
    except stripe.error.CardError as e:
        response = {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        response = {
            "error": "An error occurred: " + str(e),
            "status": status.HTTP_400_BAD_REQUEST,
        }
    return Response(response)
