from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.db.models import Q
from django.http import Http404

from .models import *
from .serializers import *


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'User Login':'user-login/',
        'Customer List':'customer-list/',
        'Customer Details':'customer-detail/<str:pk>/',
        'Customer Create':'customer-create/',
        'Customer Update':'customer-update/<str:pk>/',
        'Customer Delete':'customer-delete/<str:pk>/',
        'Product List':'product-list/',
        'Product Search':'product/?search=<param>',
        'Product Details':'product-detail/<str:pk>/',
        'Product Create':'product-create/',
        'Product Update':'product-update/<str:pk>/',
        'Product Delete':'product-delete/<str:pk>/',
        '!(Alternative) Products list':'list-products/',
        '!(Alternative) Products By Categories':'products/<slug:category_slug>/',
        '!(Alternative) Product Details':'products/<slug:category_slug>/<slug:product_slug>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def CustomerList(request):
    # print("1")
    customers = Customer.objects.all()
    #carts = Cart.objects.all()
    # print("2")
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


#Customer Login
@api_view(['POST'])
def CustomerLogin(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        customer_qs = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)    

    if password == customer_qs.password:
        serializer = CustomerSerializer(customer_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Entered wrong password!", status=status.HTTP_404_NOT_FOUND)
    

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
    print(serializer)
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


class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetails(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        

# @api_view(['GET'])
# def UserCart(request, pk):
#     print(0)
#     try:
#         customer = User.objects.get(id=pk)
#         print(1)
#         cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
#         print(1.5)
#         items = cart.cartitem_set.all()
#         #print(items)
#     except User.DoesNotExist:
#         print(2)
#         items = []


#     serializer = CartItemSerializer(items, many=True)
#     print(serializer)

#     print(3)
#     context = {'items': items}
#     print(4)
#     return Response(serializer.data, status=status.HTTP_200_OK)