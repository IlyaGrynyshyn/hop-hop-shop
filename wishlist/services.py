from django.conf import settings
from shop.models import Product
from shop.serializers import ProductSerializer


class WishlistService:
    def __init__(self, request: object) -> None:
        # Initialize the wishlist service with the request session
        self.session = request.session
        self.wishlist = self.session.get(settings.WISHLIST_SESSION_ID, [])

    def save(self) -> None:
        # Save the wishlist to the session
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        self.session.modified = True

    def add_product(self, product_id: int) -> None:
        # Check if the product_id is not already in the wishlist
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
            self.save()
        else:
            print(f"Product with ID {product_id} is already in the wishlist")

    def remove_product(self, product_id: int) -> None:
        # Remove a product from the wishlist if it's there
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            self.save()

    def clear(self) -> None:
        # Clear the entire wishlist
        self.wishlist = []
        self.save()

    def get_products(self) -> list[Product]:
        # Get a list of products in the wishlist
        products = Product.objects.filter(id__in=self.wishlist)
        return products

    def __iter__(self):
        # Iterate over the products in the wishlist, serializing each one
        products = Product.objects.filter(id__in=self.wishlist)
        for product in products:
            yield ProductSerializer(product).data
