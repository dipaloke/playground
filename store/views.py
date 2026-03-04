from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product

# Create your API views here.
@api_view(['GET','POST'])
def product_list(request):
    # return HttpResponse('ok')
    # return Response('ok')
    # query_set = Product.objects.all()
    #select related collection title
    if (request.method == 'GET'):
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many= True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
          serializer = ProductSerializer(data=request.data) # deserializing data to save the product obj to DB
        #   if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        #   else:
        #        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          serializer.is_valid(raise_exception=True)
          serializer.validated_data
          return Response('ok')


@api_view()
def product_details(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # We can get the same result with this shortcut get_object_or_404

        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


#creating view for Nesting a hyperlink to review the nested related object
@api_view()
def collection_details(request, pk):
      return Response('ok')
