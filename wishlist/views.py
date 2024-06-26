from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from shop.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


def add_to_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Product not found."}, status=404
        )

    wishlist = request.session.get("wishlist", [])
    if product_id not in wishlist:
        wishlist.append(product_id)
        request.session["wishlist"] = wishlist
    return JsonResponse({"success": True})


def remove_from_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Product not found."}, status=404
        )

    wishlist = request.session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        request.session["wishlist"] = wishlist
    return JsonResponse({"success": True})


def view_wishlist(request):
    wishlist = request.session.get("wishlist", [])
    products = Product.objects.filter(id__in=wishlist)
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({"products": serializer.data})


def clear_wishlist(request):
    request.session["wishlist"] = []
    return JsonResponse({"success": True})
