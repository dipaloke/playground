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
    queryset_products = Product.objects.all() [:5] # shows first 5 items excluding 5
    queryset_products_one = Product.objects.all() [5:10] # skips firsts 5 then shows upto 9th items -> 5 items total
    products_two = Product.objects.values('id','title') # To select necessary table columns
    products_three = Product.objects.values('id','title', 'collection__title') # returns with related fields "__"
    # only values return dictionary but with "values_list" method returns tuple
    products_four = Product.objects.values_list('id','title', 'collection__title')
    queryset_only = Product.objects.only('id', 'title') # selects columns but returns instances instead of dictionary
    queryset_defer = Product.objects.defer('description') # selects all fields except description
    queryset_preload_related_table = Product.objects.select_related('collection').all() #without preloading the related table collection the query will take a long time because it will query for individual products separately
    queryset_preload_prefetch_related = Product.objects.prefetch_related('promotions').all() # When the related table can have multiple objects (product table can have multiple promotions )
    queryset_preload_prefetch_related_select_related = Product.objects.prefetch_related('promotions').select_related('collection').all() # We can combine both methods together as both methods return a queryset




# Exercise
    customer_set_accounts = Customer.objects.filter(email__icontains='.com') # customers with '.com' in email
    collection_set_products = Collection.objects.filter(featured_product__isnull=True) # Collections without feature products
    product_Set_inventory = Product.objects.filter(inventory__lt=10) # Products with low inventory > 10
    orders_Set = Order.objects.filter(customer__id=1) # Orders placed by customer with id 1
    order_item_Set = OrderItem.objects.filter(product__collection__id=3) # Order items for products in collection 3
    #Select products that have been ordered and sort them by title
    queryset_product_ids = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by("title")
    # Get the last 5 orders with their customer and items (incl product)
    queryset_preload_orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


    return render(request, 'hello.html', {'name': "Dipaloke",
                                            # 'titles': list(queryset_one)
                                              #'products': list(queryset_five_date),
                                               'orders': list(queryset_preload_orders),
                                                })
