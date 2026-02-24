from typing import Any

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
from django.db.models.aggregates import  Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models
# from tags.models import TaggedItem
# from tags.models import TaggedItem

# Register your models here.
#Customizing the list display of the product model in the admin page

#custom filter
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10', 'Low')

        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


#Using generic relations -- Inside the add product form we want to add tags
# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [TagInline]
    # fields = ['title','slug'] # Hides other fields from Add product form
    # exclude = ['title'] # excludes provided fields from Add product form
    # readonly_fields = ['title'] # read only fields in Add product form

    prepopulated_fields = {
        'slug' : ['title']
    }    # slug field will be auto populated based on title.

    autocomplete_fields = ['collection']



    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory', "inventory_status",  'last_update', 'collection_title']
    list_editable = ['unit_price'] #allows us to edit the unit price directly from the list display
    list_select_related = ["collection"] #preloads collection related field. same as `queryset.select_Related`
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    #Adding a custom method to display the inventory status & ordering of the product as computed column
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    #Custom action clear inventory
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'membership','orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields=['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order_count')
    #Providing links to Other Pages
    def orders(self, customer):
        url = (
            # reverse('admin:app_model_page')
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

#Creating items inside order (Editing children using inline)
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields =['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
   # list_editable = ['payment_Status']
    list_per_page = 20

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'featured_product', 'product_count']
    search_fields = ['title'] # used for auto complete

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (
            # reverse('admin:app_model_page')
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, collection.product_count)
        # return collection.product_count

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )
