from django.contrib import admin
from . import models

# Register your models here.
#Customizing the list display of the product model in the admin page
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', "inventory_status",  'last_update']
    list_editable = ['unit_price'] #allows us to edit the unit price directly from the list display
    list_per_page = 10

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

admin.site.register(models.Collection)
