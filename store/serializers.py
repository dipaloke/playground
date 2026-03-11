from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Reviews


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
# class CollectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ['id', 'title']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


# class ProductSerializer(serializers.Serializer):
#     # We need to decide what fields of the product model class we need to serialize
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     # Renaming a model field to custom name
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price' )
#     #Custom serializer (we can create new fields that are not in the model class)
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     #serializing relations primary-key(id)
#     collection = serializers.PrimaryKeyRelatedField(
#         queryset=Collection.objects.all()
#     )
#     #serializing relations with string
#     collection_title = serializers.StringRelatedField(source='collection')

#     #collection object
#     collection_obj = CollectionSerializer(source='collection')

#     #Nested Hyperlink related obj (clicking the link goes to another page )
#     collection_hyperlink = serializers.HyperlinkedRelatedField(
#         queryset= Collection.objects.all(),
#         view_name = 'collection_details', # will be used as the hyperlink name. (we need to create the view in urls)
#         source='collection',
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.2)


# Serialize with Model Serializer: (Do not need to add all the object name inside model and also here)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'slug','inventory', 'unit_price','price','price_with_tax','collection','collection_title', 'collection_obj']
        # fields ='__all__' # Bad practice : Adds all of the fields of the product class

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price' )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection_title = serializers.StringRelatedField(source='collection')
    collection_obj = CollectionSerializer(source='collection')

    def calculate_tax(self, product: Product):
         return product.unit_price * Decimal(1.2)

    # collection_hyperlink = serializers.HyperlinkedRelatedField(
    #     queryset= Collection.objects.all(),
    #     view_name = 'collection_details', # will be used as the hyperlink name. (we need to create the view in urls)
    #     source='collection',
    # )

    # Over writing the default form validation
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password do not match')
    #     return data # dictionary

    #Overwrite how a product is created
    def create(self, validated_data):
        product = Product(**validated_data) # extracting the validated data
        # Now add extra fields
        product.other = 1
        product.save()
        return product

    #Overwrite how a product is updated
    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'date', 'name', 'description']

    # we want to overwrite the create method so we can get the product id from url sent from views via context
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id=product_id, **validated_data)
