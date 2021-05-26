from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many=True)

    class Meta:
        model = OrderItem_v2
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True)
    address = ShippingAddressSerializer(many=True)

    class Meta:
        model = Order_v2
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    #products = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True)
    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'

class CustomerSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
    
# class UserSerializer(serializers.ModelSerializer):
#     customers = CustomerSerializer(many=True)

#     class Meta:
#         model = User
#         fields = '__all__'