from rest_framework import serializers
from .models import *


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    #orderItems = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    #orders = OrderSerializer(many=True)
    #shippingAddresses = ShippingAddressSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'
