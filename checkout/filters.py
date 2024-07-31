import django_filters

from checkout.models import Order


class OrderFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")

    class Meta:
        model = Order
        fields = ["id"]
