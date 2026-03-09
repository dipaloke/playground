from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection, OrderItem
from django.db.models.aggregates import Count
from rest_framework.views import APIView


from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

# Create your API views here.

#Class Based views
# class ProductList(APIView):
#      def get(self, request):
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set, many= True, context={'request': request})
#         return Response(serializer.data)

#      def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# Using GENERIC VIEWS
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     # def get_queryset(self): # We only need to overwrite the methods only if we are going to add custom logics to these method.
#     #     return Product.objects.select_related('collection').all()

#     serializer_class = ProductSerializer
#     # def get_serializer_class(self):
#     #     return ProductSerializer()
#     def get_serializer_context(self):
#         return {'request': self.request}

#Function based views
# @api_view(['GET','POST'])
# def product_list(request):
#     # return HttpResponse('ok')
#     # return Response('ok')
#     # query_set = Product.objects.all()
#     #select related collection title
#     if (request.method == 'GET'):
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set, many= True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#           serializer = ProductSerializer(data=request.data) # deserializing data to save the product obj to DB
#         #   if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         #   else:
#         #        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#           serializer.is_valid(raise_exception=True)
#           serializer.save()
#           # serializer.validated_data
#           return Response(serializer.data, status=status.HTTP_201_CREATED)

#Class View
# class ProductDetails(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data,)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({
#                        'error': 'Product can not be deleted as it associated with an order'
#             },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Converting the GEneral Class view to the Customized Generic class view with Concrete View Classes
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({
#                        'error': 'Product can not be deleted as it associated with an order'
#             },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def get_serializer_context(self):
#         return {'request': self.request}


# Using ViewSets writing multiple related views

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')

        if OrderItem.objects.filter(product_id=product_id).exists():
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({
    #                    'error': 'Product can not be deleted as it associated with an order'
    #         },status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




# function view
#To  get, update, delete a product
# @api_view(['GET', 'PUT','DELETE'])
# def product_details(request, id):
#     # try:
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)

#     # We can get the same result with this shortcut get_object_or_404
#         product = get_object_or_404(Product, pk=id)
#         if request.method == 'GET':
#             serializer = ProductSerializer(product, context={'request': request})
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#              serializer = ProductSerializer(product, data=request.data,)
#              serializer.is_valid(raise_exception=True)
#              serializer.save()
#              return Response(serializer.data)
#         elif request.method == 'DELETE':
#              if product.orderitems.count() > 0:
#                   return Response({
#                        'error': 'Product can not be deleted as it associated with an order'
#                   },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#              product.delete()
#              return Response(status=status.HTTP_204_NO_CONTENT)


#creating view for Nesting a hyperlink to review the nested related object
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# Converting collection_list view from function to Class View using the Generic ConCreate view classes
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#             products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Customized Generic class view

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(
#         Collection.objects.annotate(
#             products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(
    #     Collection.objects.annotate(
    #         products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
