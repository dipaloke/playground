Practice project

### Django Fundamentals:

- pipenv install django
- pipenv shell → activates venv
- django-admin startproject playground → creates project named playground
- python [manage.py](http://manage.py) runserver → ([manage.py](http://manage.py) same as django-admin)
- python [manage.py](http://manage.py) startapp appname → creates new app
- After creating each app. Need to add the app inside [settings.py](http://settings.py)
- Views are the Req handler (request → view functions() → response)
- Debug mode can be used to debug django functions
- [Debug toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) can be set up for debugging

### Building a Data Model:

- Objective:
    - Intro to Data Modeling
    - Building a E-Commerce Data Model
    - Organizing models in apps
    - Coding model classes

#### Intro to Data Modeling
- **Relationships**: One to one, One to many, many to one.
- Instead of making a big app with all the models (blotted app) we break it into multiple smaller apps.
- Ecommerce -> Product, Customers, Carts, Orders (poor way to separate apps)
-  Orders app is dependent on carts app and customers app, Carts app is dependent on the Products app. So if we update one app another app could break changes.
- All concepts are highly related should bundled together.
- Store -> Product, Collection, Tag, Customer, Cart, Cart Item, Order, Order Item (blotted app: bad idea)
- We will find middle ground by separating TAGS as another app as it has separate functionality (Tag, Tag Item: can be product, video anything abstract )
- Every peace of app is self-contained and provides a separate peace of functionality.
- Both app have ZERO COUPLING, so we can update and deploy them separately without breaking any changes in other app.
- So not blotted, Minimal Coupling, High Cohesion(Focus)
- Every app should focus on a functionality and should include all the functionality needed to fulfill the functionality. (python manage.py startapp store, tags)

#### Building a E-Commerce Data Model
- [Model fields and types](https://docs.djangoproject.com/en/6.0/topics/db/models/#)
- [Choices](https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.Field.choices)
-  (**One to One relationship**)[]
	- Child to parent relation.
	- We only need to define relation in the child... Parent will automatically get the relation (reverse relation).
	-  `models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)`
		- notNull = when field accepts null
		- PROTECT = cant delete parent without deleting child
		- default = returns default value
		- CASCADE = when parent is deleted child will be deleted too.
		- If primary key is not set django will create a id field automatically and it will be one to many relationship with addresses (one customer many address)
- **One to Many relationship**
	- `customer = models.ForeignKey(Customer, on_delete=models.CASCADE)`
	- Just remove `oneToOneField` and `primary_key=True`, instead set the field as `ForeignKey` and we have one to many relationship. (one customer multiple address)
	-  While defining the one to many relations, we can add the parent class before the child or we can mention the parent within "" and this also works but will not update the model name when the related model class name is changed.
	-  In Django, a **one-to-many relationship** is defined by placing a `ForeignKey` on the model that represents the “many” side (e.g. Products), pointing to the “one” side (e.g. Collection).
- **Many to Many relationship**
	- any  product can have multiple promotions also a promotion can contain multiple products.
	- We can specify the relation in any model and Django will create the reverse relation automatically.
	- `Product:`
		  `promotions = models.ManyToManyRel(Promotion)`
- **Circular relationship Dependency**
	- Happens when two model class ususes foreign key to have many to many relationship with each other. (depends on each other on the same time.)
	- such as Product class and Collection class depends on each other on the same time.
	- Two choices to fix the error:
		- One is to rename the **related_name='something else'**
		- or **related_name='+'** tells Django to not to create the reverse relationship.
- **Generic relationships**: (content_type, object_id, content_object)
- Bad way:
	-  is to make the app dependent on the other app from where we want to read the model class:  directly import `from store.models import Product`  and use as `product = models.ForeignKey(Product)`
- Good way:
	- With **contentType** model we can determine the generic relations between models imported from `from django.contrib.contenttypes.models import ContentType` `Content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)`
	- Then defining the ID of the expected table (Here we are assuming the ID field of the  table from another app is integer ) `object_id = models.PositiveBigIntegerField()`
	- Then we define the content Object to read the actual object from the other table with  Generic Foreign key imported from `from django.contrib.contenttypes.fields import GenericForeignKey` defined as `content_object = GenericForeignKey()`

### Setting Up the DataBase
- Creating migrations
- Running migrations
- Reversing migrations
- Populating the database

#### Migrations:
- `python manage.py makemigrations`  `python manage.py migrate` `python manage.py sqlmigrate`
- After each model change we have to run the command and migration file can be found for each app under migration folder.
- If we want to change migration file name we need to change the name everywhere related to the dependent file.
- If we don't provide default value while migrating we will be asked for options to cancel or provide default value on terminal.  if we choose option 2 and provide default value, it will be applied to migration once and the model will be same as before
#### Customizing Database schema
-  [Meta model : ](https://docs.djangoproject.com/en/6.0/ref/models/options/)
- Revert back migrations: `python manage.py migrte {app name} {migration number}`
- mockaroo.com --> for mock data
- Installed mysql for windows and opened with Dbeaver
-
### Django ORM
- [Query sets](https://docs.djangoproject.com/en/6.0/ref/models/querysets/)
Topics:
- Introduction to Django ORM
- Querying and manipulating data
- Filtering data
- Sorting Data
- Grouping Data

#### Introduction to ORM
- reduce complexity in code
- Make the code more understandable
- Help us get done in less time

- In Django ORM we need to first understand the term **Manager** & **Querysets**
	- Every model has an attribute called "Objects" which returns a "manager"
		- A **Manager** is an **interface** to the database.
		- The Manager has a bunch of  methods for querying and updating data .
			- Most of these methods **e.g. : `Product.objects.all()`** method return a **query set** .
			- In contrast we have some other methods that return result immediately. **e.g. `Product.objects.Count()`** returns number of all the records in Products table.
#### Methods:
- **Retrieving Objects**:
	-  `.all()` :  `queryset = Product.objects.all()`
	- **Returns single entry obj**:  `objects.get(id=1)` / `get(pk=1)` --> primary key (automatically translates the primary key)
		- get() will throw exceptions if the product is not found
		- So we need to handle the exception using try catch block
	- To avoid using try catch block we are going to use the **`filter`** method which return a **querystring**:
		- `product = Product.objects.filter(pk=0).first()`
	- To check product **exists** or not we use `.exists()` method:
		- `exists = Product.objects.filter(pk=0).exists()`

- [**Filtering Objs with Lookups :**](https://docs.djangoproject.com/en/6.0/ref/models/querysets/)
	- [Field Lookups](https://docs.djangoproject.com/en/6.0/ref/models/querysets/#field-lookups)
		- By using **`__get`** lookup we can select product price grater then the passed value:
			- `queryset = Product.objects.filter(unit_price__gt=20)`
		- using **`__range`** we can select a range of products:
			- `queryset_one = Product.objects.filter(unit_price__range=(20, 30))`
		- We can also filter across relationships example: we want to find all the products in collection no 1 : **`collection__id(attributes or fields of collection class)__range(lookuptype)=1`**
			- `queryset_two = Product.objects.filter(collection__id__range=(1, 2, 3))`
		- For strings:
			- `queryset_three = Product.objects.filter(title_contains='coffee')` **case sensitive**
			- **case insensitive:**
				- `queryset_three = Product.objects.filter(title__icontains='coffee')`
		- **For Dates:**
			- to find all the products updated at 2021:
				- `queryset_five_date = Product.objects.filter(last_update__year=2021)`
					- We can also find individual components like year, month, day etc.
		- **Null type : **
			- To find products without description we use null type:
				- `queryset_six_null = Product.objects.filter(description__isnull=True)`
		- **Filter with 2 argument  & Chain 2 filters:** We can also pass two argument inside filter method: EX: select all the products inventory < 10 **AND** price < 20
			- `querySet = Product.objects.filter(inventory__lt=10, unit_price___lt=20)`
			- `querySet = Product.objects.filter(inventory__lt=10).filter(unit_price___lt=20)` --> Works as end operator in sql.
		- **Q Operator :** (query)
			- using this **Q** class we can represent a pis of query that contain a value
			- `from django.db.models import Q`
			- select all the products inventory < 10 **OR** price < 20
			- `querySet = Product.objects.filter(Q(inventory__lt=10))`
				- Here every **Q** obj incapsulates a keyword argument/query expression
				- We can combine more **Q** obj with bitwise operators:
					- `querySet = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))`
						- The **|** operator works as **SQL** **OR**
			-  **&** --> AND **~** --> NOT
				- Inventory less then 10 **AND** unit price is **NOT** less then 20
				- `querySet = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))`
	- **F OBJECT :** Referencing field with f obj
		- When we need to compare two fields:
		- `from django.db.models import F`
		- Where inventory = unit Price
		- `queryset = Product.objects.filter(inventory=F('unit_price)`
		- Using F class we can also define a Field and a related table:
			- We compare inventory of a product with Id of its collection:
			- `queryset = Product.objects.filter(inventory=F('collection__id)`
- **SORTING DATA :**
	- **order_by :** Using this method we can pass one or two argument to sort data:
		- `queryset = Product.objects.order_by('title)` --> ascending order
		- `queryset = Product.objects.order_by('-title)` --> descending order
		- **Multiple field :**
			- `queryset = Product.objects.order_by('unit_price','-title)` --> sort products for unit price in ascending order and title in descending order
			- **reverse:** Reverses the ascending and descending order:
			- `queryset = Product.objects.order_by('unit_price','-title).reverse()`
	- **Orderby** is also the method of queryset obj so we can use then after filter:
		- Collect all the products in collection 1 and order by their unit price.
		- `queryset = Product.objects.filter(collection__id=1).order_by('unit_price)`
	- Order the objets and accessing the 1st obj:
		- `product = Product.objects.order_by('unit_price)[0]` --> not a query set
	- **Earliest method** --> does same as before but returns a obj instead of queryset:
		- `product = Product.objects.earliest('unit_price')` --> ascendending orders and 1st obj
	- **latest method :**
		- `product = Product.objects.latest('unit_price')` --> descending orders and 1st obj
- **LIMITING RESULTS :** 3/02/26
	- To limit  the result of the array we can user pythons **Array slicing syntax**.
		- `products = Product.objects.all()[:5]` -> shows first 5 items excluding 5
		- `products = Product.objects.all()[5:10]` -> skips firsts 5 then shows upto 9th items -> 5 items total
- **Specify query using values method :**
	- Sometimes its necessary to skip some columns of a table. We can do that by using **`values method**:
		- `products = Product.objects.values('id', 'title')`
	- We can also select values of related fields with `__` :
		-  `products = Product.objects.values('id', 'title', 'collection__title')`
	- When using the **values method** we need to understand that we will get a bunch of dictionary as a result.
	- To get a tuple instead of Dictionary we can use the method **`values_list`** method.
	- **EXERCISE :**
		-  Select products that have been ordered and sort them by title
		- ` queryset_product_ids = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by("title")`
- **Deferring Fields :**
	- With **only** method we can do same as **values** method but instead of dictionary **only** method returns instances.
		- `queryset = Product.objects.only('id','title')`
	- Need to be sure when using "**only/defer**" method because we can end up with a lot of query if we don't know what we are doing (calling this methods inside for loop(queries for all the products individually and takes a lot of time)).
	- With **defer** method we can create a query such that it will select all the columns except the column provided with defer.
		- `queryset = Product.objects.defer('description')`
- **Selecting Related Tables (select_related (1), prefetch_related (n)) :**
	- Sometimes we need to preload a bunch of objects together as django will query for only 0ne table and will not query related tables if we dont say so:
		- `queryset = Product.objects.all()` --> When
			- ```
			  <ul>
			      {%for product in products %}
			      <li>{{ product.title }} - {{product.collection.title}}</li>
			      {% endfor %}

			   </ul>
			  ```
			  - loading this query takes a longer time because django will search for every product (Product table) not going to related tables (collection table).
			- So we want to preload the Collection fields
				- `queryset = Product.objects.select_related(`'collection').all()`
		- When using **`select_related`** method django creates a join between tables.
		- We can also span relationships here and preload them:
			- `queryset = Product.objects.select_related(`'collection__someOtherfield').all()`
- **Prefetch_related :**
	- We use **`prefetch related`** when we know the current relation with the  related table has multiple objects, for single objects `select_Relted`:  (the product model can have one collection(`select_related`) but multiple `Promotions` (`prefetch_related`) )
		- `queryset_preload_prefetch_related = Product.objects.prefetch_related('promotions').all()`
- **Aggregating Objects :**
	- We use it to find summaries like min max avg price of our product.
	- To count all the products we should use id inside the Count if we use description we only get  the products who have description != null.
		- `result_dict_aggregate= Product.objects.aggregate(count=Count('id'))`
- **Annotate Method for adding additional attributes : **
	- We will user annotate method while querying objects with additional attributes
		- **EXPRESSION :**
			- Value, F, Func, Aggregate
				- `queryset_annotate_id = Customer.objects.annotate(new_id=F('id') + 1)`
- **Database Function :**
	-  [Documentation](https://docs.djangoproject.com/en/6.0/ref/models/database-functions/)
	- Using db functions we can easily **concat** first and last name of a customer.
		```
		queryset_db_func = Customer.objects.annotate(

        #CONCATENATE first name and Last name

        full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')

    )
		```
		- Short form:
		```
		queryset_db_func_concat_Short = Customer.objects.annotate(

        #CONCATENATE first name and Last name

        full_name = Concat('first_name', Value(' '), 'last_name')

    )
		```
- **Grouping Data**
	- `queryset_db_func_count = Customer.objects.annotate(order_Count = Count('order'))`

### Recap:
- **Expression:**
	- Base type for all type of expression
	- Derivative of the class
		- **Value :**
			- for representing simple values like Boolean, a number, a string.
		- **F :**
			- for referencing fields
		- **Func :**
			- for calling DB functions
		- **Aggregate :**
			- Base class for all aggregate classes like count, sum and so on.
		- **Expression wrapper :**
			- Use this class while building complex expression.
- **Expression Wrapper :**
	- Expression wrapper is used to perform calculations on the fields of the model. For example, we can calculate the total price of an order by multiplying the quantity of the product with its unit price and then we can annotate this total price to the order queryset.
		- `queryset_expression_wrapper = Product.objects.annotate(discounted_price=ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField()))`
- **Querying  Generic Relationship :**
	- In our application we have created the **TAG** app separately (generic app: not dependent on other models). So how can we find the tags of each product?
		- In the DB we have a default table called `django_content_type`
		-     To find the content type of a modal and then we can use that content type to get the instances of that model.
			- `content_type = ContentType.objects.get_for_model(Product)`
		- to get all the tags for the product with id 1
			- `queryset_product_tags= TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1)`

