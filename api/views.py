from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Customer, Product
from .serializers import CustomerSerializer, ProductSerializer


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Search':'/product/search=<str:param>',
        'Categorical Search':'/product/search=<str:category>/<str:param>',
        'List':'/customer-list/, /product-list/',
        'Detail':'/customer-detail/<str:pk>/, /product-detail/<str:pk>/',
        'Create':'/customer-create/, /product-create/',
        'Update':'/customer-update/<str:pk>/, /product-update/<str:pk>/',
        'Delete':'/customer-delete/<str:pk>/, /product-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def CustomerList(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def CustomerDetail(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #Get Customer detail
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)
       
#Create customer
@api_view(['POST'])
def CustomerCreate(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Update a customer
@api_view(['POST'])
def CustomerUpdate(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete a customer
@api_view(['DELETE'])
def CustomerDelete(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    customer.delete()    
    return Response(status=status.HTTP_204_NO_CONTENT)

#Product APIs
#Product search
@api_view(['GET'])
def ProductSearch(request, param):
    try:
        product = Product.objects.filter(name__icontains=param)
        
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Product search based on category
@api_view(['GET'])
def ProductCategoricalSearch(request, category, param):
    try:
        product = Product.objects.filter(category=category).filter(name__icontains=param)
        #product = first_qs.objects.filter(name__icontains=param)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

        
@api_view(['GET'])
def ProductList(request):    
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ProductDetail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def ProductCreate(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ProductUpdate(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(instance=product, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def ProductDelete(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
