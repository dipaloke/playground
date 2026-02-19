from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
from django.db.models.aggregates import  Count
from django.utils.html import format_html

# Register your models here.
#Customizing the list display of the product model in the admin page
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', "inventory_status",  'last_update', 'collection_title']
    list_editable = ['unit_price'] #allows us to edit the unit price directly from the list display
    list_select_related = ["collection"] #preloads collection related field. same as `queryset.select_Related`
    list_per_page = 10

    def collection_title(self, product):
        return product.collection.title

    #Adding a custom method to display the inventory status & ordering of the product as computed column
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'membership']
    list_editable = ['membership']
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
   # list_editable = ['payment_Status']
    list_per_page = 20

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        return collection.product_count

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )
