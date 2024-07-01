from django.shortcuts import get_object_or_404
from shop.models import Product


class FavouriteService:
    def __init__(self, session):
        self.session = session
        self.favourites = session.get("favourites", [])

    def save(self):
        self.session.modified = True

    def add_product(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        if product_id not in self.favourites:
            self.favourites.append(product_id)
            self.session["favourites"] = self.favourites
            self.save()
        return product

    def remove_product(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        if product_id in self.favourites:
            self.favourites.remove(product_id)
            self.session["favourites"] = self.favourites
            self.save()
        return product

    def clear(self):
        self.session["favourites"] = []
        self.favourites = []
        self.save()

    def get_products(self):
        return Product.objects.filter(id__in=self.favourites)
