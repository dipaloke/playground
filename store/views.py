from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product

# Create your API views here.
@api_view()
def product_list(request):
    # return HttpResponse('ok')
    # return Response('ok')
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many= True)
    return Response(serializer.data)

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
