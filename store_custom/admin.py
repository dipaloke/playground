from django.contrib import admin
# Extending Pluggable apps (extending tag app)
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from products.model import Product

# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItem]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
