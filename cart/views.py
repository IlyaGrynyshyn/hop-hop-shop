from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from shop.models import Product


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class AddToCartView(APIView):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)

        product = get_object_or_404(Product, id=product_id)
        if product.stock <= 0:
            return Response(
                {"error": "Product out of stock"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect("cart_detail")


class UpdateCartView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart = get_object_or_404(Cart, session_key=session_key)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs["item_id"])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        new_quantity = request.data.get("quantity", instance.quantity)
        if instance.product.stock < new_quantity:
            return Response(
                {"error": "Not enough stock available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if request.user.is_authenticated:
            if cart_item.cart.user == request.user:
                cart_item.delete()
        else:
            session_key = request.session.session_key
            if cart_item.cart.session_key == session_key:
                cart_item.delete()
        return redirect("cart_detail")


class CheckoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = get_object_or_404(Cart, session_key=session_key)

        if cart.items.count() == 0:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            for cart_item in cart.items.all():
                if cart_item.product.stock < cart_item.quantity:
                    return Response(
                        {"error": f"Not enough stock for {cart_item.product.name}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            cart.items.all().delete()

        return Response(
            {"success": "Order placed", "order_id": order.id}, status=status.HTTP_200_OK
        )
