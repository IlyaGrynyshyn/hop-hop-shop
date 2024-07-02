from django.conf import settings
from shop.models import Product


class WishlistService:

    def __init__(self, request):
        self.session = request.session
        self.wishlist = self.session.get(settings.WISHLIST_SESSION_ID, [])

    def save(self):
        self.session.modified = True

    def add_product(self, product):
        if product.id not in self.wishlist:
            self.wishlist.append(product.id)
            self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
            self.save()
        return product

    def remove_product(self, product):
        if product.id in self.wishlist:
            self.wishlist.remove(product.id)
            self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
            self.save()
        return product

    def clear(self):
        self.session[settings.WISHLIST_SESSION_ID] = []
        self.wishlist = []
        self.save()

    def get_products(self):
        return Product.objects.filter(id__in=self.wishlist)
