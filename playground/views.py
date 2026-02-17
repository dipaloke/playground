from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import  Max, Min, Avg, Sum
from django.db.models import Value, F, Func, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType #represents the content type table in the database which is used to store the information about the models in the application. It has fields like app_label, model and id which are used to identify the model and its instance. We can use this model to get the content type of a model and then we can use that content type to get the instances of that model. For example, if we want to get all the products in our application, we can get the content type of the product model and then we can use that content type to get all the products in our application.
from django.db import transaction
from django.db import connection


from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order
from store.models import OrderItem
from tags.models import TaggedItem
from store.models import Cart, CartItem


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

    result_dict_aggregate= Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price')) #used when we need to find summaries such as min max avg

    result_queryset_aggregate= Product.objects.filter('collection__id').aggregate(count=Count('id'), min_price=Min('unit_price')) #used when we need to find summaries such as min max avg

    queryset_annotate = Customer.objects.annotate(is_new=Value(True)) # annotate is used to add new field to the queryset and value is used to assign value to that field. Here we are adding a new field called is_new and assigning it a value of True for all customers. We can also use annotate to calculate the number of orders for each customer by using Count('order') and then we can filter customers who have more than 5 orders by using filter(order_count__gt=5)

    queryset_annotate_id = Customer.objects.annotate(new_id=F('id') + 1)

    queryset_db_func = Customer.objects.annotate(
        #CONCATENATE first name and Last name
        full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )

    queryset_db_func_concat_Short = Customer.objects.annotate(
        #CONCATENATE first name and Last name
        full_name = Concat('first_name', Value(' '), 'last_name')
    )

    #number of orders each customer has placed
    queryset_db_func_count = Customer.objects.annotate(order_Count = Count('order'))

    #Expression wrapper is used to perform calculations on the fields of the model. For example, we can calculate the total price of an order by multiplying the quantity of the product with its unit price and then we can annotate this total price to the order queryset.
    queryset_expression_wrapper = Product.objects.annotate(discounted_price=ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField()))

    # to find the content type of a modal and then we can use that content type to get the instances of that model.
    content_type = ContentType.objects.get_for_model(Product)
    queryset_product_tags= TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1) # to get all the tags for the product with id 1

    queryset_product_tags_custom_manager = TaggedItem.objects.get_tags_for(Product, 1) #Custom manager to get all the tags fot a specific product

    queryset_caching = Product.objects.all() # to cache the queryset in memory and then we can use it to perform multiple operations on it without hitting the database multiple times. This is useful when we need to perform multiple operations on the same queryset and we want to avoid hitting the database multiple times.
    queryset_caching[0]

    #Creating a new collection
    collection = Collection()
    collection.title = "video Games"
    collection.featured_product = Product(pk=1)
    collection.save()

    #Creating collection shorter way
    collection_new = Collection.objects.create(title='Video Games', featured_product_id = None)

    #Updating a collection
    Collection.objects.filter(pk=11).update(featured_product_id = 1)

    #Deleting single or multiple collections
    collection_delete = Collection(pk=11)
    collection_delete.delete()
    #multiple delete
    delete_queryset = Collection.objects.filter(pk__in=[11, 12, 13]).delete()

    #transaction with partial section
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = item.product.unit_price
        item.save()

    #Raw SQL
    queryset_raw_sql = Product.objects.raw('SELECT * FROM store_product')

    #Bypass the ORM and execute raw SQL directly without model
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
        raw_sql_result = cursor.fetchall() #returns a list of tuples containing the results of the query. Each tuple represents a row in the result set, and the values in the tuple correspond to the columns in the result set. We can also use cursor.fetchone() to get a single row from the result set or cursor.fetchmany(size) to get a specific number of rows from the result set.

        


#Transactions (Need to save all the operations in a transaction block to ensure that either all the operations are successful or none of them are successful. This is useful when we need to perform multiple operations on the database and we want to ensure that the database is in a consistent state.)
@transaction.atomic
def create_order(request):
    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = item.product.unit_price
    item.save()











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

    #How many orders do we have
    result = Order.objects.aggregate(count=Count('id'))

    #How many units of product 1 have we sold?
    result_units = Order.objects.filter(product__id=1).aggregate(unit_sold=Sum('quantity'))

    #How many orders has the customer one placed
    result_orders = Order.objects.filter(customer__id=1).aggregate(count=Count('id'))

    #What is the min, max and avg price of products in collection 1?
    result_price = Product.objects.filter(collection_id=3).aggregate(min_price=Min('unit_price'), avg_price=Avg('unit_price'), max_price=Max('unit_price'))

    #Customers with their last order ID
    customers_last_order_id = Customer.objects.annotate(last_order_id=Max('order__id'))

    #Collections and count of their products
    collection_product_count = Collection.objects.annotate(products_count=Count('product'))

    #Customers with more than 5 orders
    customers_with_five_orders = Customer.objects.annotate(orders_count=Count('order')).filter(orders_count__gt=5)

    #Customers & their total spending
    customers_total_spending = Customer.objects.annotate(total_Spent=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')))

    #Top 5 best-selling products and their total sales
    best_Selling_products = Product.objects.annotate(total_sales=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))).order_by('-total_sales')[:5]

    #Create a shopping cart with an item
    cart = Cart()
    cart.save()

    item1 = CartItem()
    item1.cart = cart
    item1.product_id = 1
    item1.quantity = 1
    item1.save()

    #Updating the quantity if an item
    item1 = CartItem.objects.get(pk=1)
    item1.quantity = 2
    item1.save()

    #Removing a cart
    cart = Cart(pk=1)
    cart.delete()



    return render(request, 'hello.html', {'name': "Dipaloke",
                                            # 'titles': list(queryset_one)
                                              #'products': list(queryset_five_date),
                                               # 'orders': list(queryset_preload_orders),
                                            #    'Product_counts':  result_queryset_aggregate ,
                                               # 'result': result_dict_aggregate,
                                               'result': queryset_annotate,
                                                })
