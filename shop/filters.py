import django_filters
from shop.models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__id", lookup_expr="iexact"
    )
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category"]
