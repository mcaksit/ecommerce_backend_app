from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer,ProductSerializer
from .models import Customer,Product

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
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
    return Response(serializer.data)

@api_view(['GET'])
def CustomerDetail(request, pk):
    customers = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CustomerCreate(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def CustomerUpdate(request, pk):
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def CustomerDelete(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()

    return Response('Customer Deleted Successfully!')

#Product APIs
@api_view(['GET'])
def ProductList(request):    
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ProductDetail(request, pk):
    try:
        products = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(f"No product exists with id: {pk}")

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def ProductCreate(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def ProductUpdate(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(f"No product exists with id: {pk}")

    serializer = ProductSerializer(instance=product, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)   


@api_view(['DELETE'])
def ProductDelete(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(f"No product exists with id: {pk}")
    
    product.delete()

    return Response('Product Deleted Successfully!')     