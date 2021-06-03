from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import *


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['name', ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


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
        # fields = '__all__'
        exclude = ('user', )

class CustomerSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     customer = CustomerSerializer()

#     class Meta:
#         model = User
#         fields = '__all__'
# exclude = ('field1', )

    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'customer']