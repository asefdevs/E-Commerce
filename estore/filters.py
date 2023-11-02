
from django_filters import rest_framework as filters
from estore.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    order_by = filters.OrderingFilter(
        fields=(
            ('price', 'Price'),

        )
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'brand']
