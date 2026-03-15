from django_filters.rest_framework import FilterSet
from .models import Product


#Creating custom filtering from the installed pkg Django-filter
# https://django-filter.readthedocs.io/en/stable/
# For this particular language this package understand we need to understand the doc

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'], #We wil;l exactly match this filed
            'unit_price': ['gt', 'lt']
        }
