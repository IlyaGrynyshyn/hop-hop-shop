from decimal import Decimal
from django.conf import settings

from shop.models import Product


class CartService:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Add a product to the cart or update its quantity
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        # If the product is not already in the cart, add it with initial quantity and price
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        # Update the quantity of the product
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def subtraction_quantity(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]["quantity"] == 1:
                del self.cart[product_id]
            else:
                self.cart[product_id]["quantity"] -= 1
        self.save()

    # Mark the session as modified to ensure it is saved
    def save(self):
        self.session.modified = True

    # Remove a product from the cart
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    # Return the total number of items in the cart
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    # Get the total price of all items in the cart
    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    # Get the total number of items in the cart
    def get_total_item(self):
        return sum(item["quantity"] for item in self.cart.values())

    # Clear the cart by deleting it from the session
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
