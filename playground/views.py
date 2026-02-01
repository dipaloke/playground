from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order
from store.models import OrderItem

# Create your views here.

def say_hello(request):
    queryset = Product.objects.all() # returns query set
    # try:
    #    product = Product.objects.get(pk=1)  # Returns single entry obj
    # except ObjectDoesNotExist:
    #     pass
    # To avoid using the try catch block and to avoid handling exception
    product = Product.objects.filter(pk=0).first() # return none if no product found . No exception
    # To check product exists or not
    exists = Product.objects.filter(pk=0).exists() #$ returns boolien
    #Filtering objs with lookups:
    #queryset = Product.objects.filter(unit_price__gt=20) # __gt is grater then lookup
    queryset_one = Product.objects.filter(unit_price__range=(20, 30)) # range lookup to find product in a range
    queryset_two = Product.objects.filter(collection__id__range=(1, 2, 3)) # filter across relationships (to find products in 1 2 3 collections)
    queryset_three = Product.objects.filter(title__contains='coffee') # filter across relationships (to find products that have coffee in their title)
    queryset_four_string = Product.objects.filter(title__icontains='coffee') #(not case sensitive) filter across relationships (to find products that have coffee in their title)
    queryset_five_date = Product.objects.filter(last_update__year=2021) # find all the products updated at 2021
    queryset_six_null = Product.objects.filter(description__isnull=True) # To find all the products without description


# Exercise
    customer_set_accounts = Customer.objects.filter(email__icontains='.com') # customers with '.com' in email
    collection_set_products = Collection.objects.filter(featured_product__isnull=True) # Collections without feature products
    product_Set_inventory = Product.objects.filter(inventory__lt=10) # Products with low inventory > 10
    orders_Set = Order.objects.filter(customer__id=1) # Orders placed by customer with id 1
    order_item_Set = OrderItem.objects.filter(product__collection__id=3) # Order items for products in collection 3

    return render(request, 'hello.html', {'name': "Dipaloke",
                                            # 'titles': list(queryset_one)
                                              #'products': list(queryset_five_date),
                                               'customers': list(customer_set_accounts)
                                                })
