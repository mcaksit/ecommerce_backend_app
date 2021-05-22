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
        'User List':'user-list/',
        'User Details':'user-detail/<str:pk>/',
        'User Create':'user-create/',
        'User Update':'user-update/<str:pk>/',
        'User Delete':'user-delete/<str:pk>/',
        'User Login':'user-login/',
        'Product List':'product-list/',
        'Product Search':'product/?search=<param>',
        'Product Details':'product-detail/<str:pk>/',
        'Product Create':'product-create/',
        'Product Update':'product-update/<str:pk>/',
        'Product Delete':'product-delete/<str:pk>/',
        '!(Alternative) Products list':'list-products/',
        '!(Alternative) Products By Categories':'products/<slug:category_slug>/',
        '!(Alternative) Product Details':'products/<slug:category_slug>/<slug:product_slug>/',
        'Cart Details':'cart-details/<int:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def UserList(request):
    print("1")
    users = User.objects.all()
    carts = Cart.objects.all()
    print("2")
    serializer = UserSerializer(carts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def UserDetail(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #Get User detail
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
       
#Create user
@api_view(['POST'])
def UserCreate(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#User Login
@api_view(['POST'])
def UserLogin(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user_qs = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)    

    if password == user_qs.password:
        serializer = UserSerializer(user_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Entered wrong password!", status=status.HTTP_404_NOT_FOUND)
    

#Update a user
@api_view(['POST'])
def UserUpdate(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete a user
@api_view(['DELETE'])
def UserDelete(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    user.delete()    
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
        

@api_view(['GET'])
def UserCart(request, pk):
    print(0)
    try:
        customer = User.objects.get(id=pk)
        print(1)
        cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
        print(1.5)
        items = cart.cartitem_set.all()
        #print(items)
    except User.DoesNotExist:
        print(2)
        items = []


    serializer = CartItemSerializer(items, many=True)
    print(serializer)

    print(3)
    context = {'items': items}
    print(4)
    return Response(serializer.data, status=status.HTTP_200_OK)