from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    # We need to decide what fields of the product model class we need to serialize
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # Renaming a model field to custom name
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price' )
    #Custom serializer (we can create new fields that are not in the model class)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    #serializing relations primary-key(id)
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    #serializing relations with string
    collection_title = serializers.StringRelatedField(source='collection')

    #collection object
    collection_obj = CollectionSerializer(source='collection')

    #Nested Hyperlink related obj (clicking the link goes to another page )
    collection_hyperlink = serializers.HyperlinkedRelatedField(
        queryset= Collection.objects.all(),
        view_name = 'collection_details', # will be used as the hyperlink name. (we need to create the view in urls)
        source='collection',
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.2)
