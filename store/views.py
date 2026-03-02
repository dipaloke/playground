from django.shortcuts import render
from django.http import HttpResponse

# Create your API views here.

def product_list(request):
    return HttpResponse('ok')
