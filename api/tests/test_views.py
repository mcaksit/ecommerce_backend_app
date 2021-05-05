import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import User, Product
from ..serializers import UserSerializer, ProductSerializer


#Initialize client
client = Client()
"""Test For User Views"""
class UserTestCase(APITestCase):

    def setUp(self):
        self.staticUser = User.objects.create(
            name="staticname",surname="staticsurname",phone="1234",email="static@test.com"
        )
        User.objects.create(
            name="person",surname="persurname",phone="12324",email="stpersonc@test.com"
        )
        self.valid_user = {
            "role" : "standard",
            "username":"testsurname",
            "password":"1234",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }

        role = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)

        self.invalid_user = {
            "role" : "standard",
            "username":"",
            "password":"",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.valid_user_update = {
            "role" : "standard",
            "username":"testname(updated)",
            "password":"nani",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.invalid_user_update = {
            "name":"",
            "surname":"",
            "phone":"",
            "email":""
        }
    #Test get all Users' details
    def test_get_all_user(self):
        response = self.client.get(reverse("user-list"))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    #Test valid User's detail 
    def test_get_valid_user(self):
        response = self.client.get(
            reverse("user-detail", kwargs={'pk':self.staticUser.pk}))
        user = User.objects.get(pk=self.staticUser.pk)
        serializer = UserSerializer(user)

        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test invalid User's detail
    def test_get_invalid_user(self):
        response = self.client.get(
            reverse("user-detail", kwargs={'pk':100}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #Test User create
    def test_create_user(self):
        response = self.client.post(
            reverse("user-create"), 
            data=json.dumps(self.valid_user),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post(
            reverse("user-create"),
            data=json.dumps(self.invalid_user),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    #Test user update
    def test_update_user(self):
        response = self.client.post(
            reverse("user-update", kwargs={'pk':self.staticUser.pk}),
            data=json.dumps(self.valid_user_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    #Test invalid updates wrong id/empty data
    def test_update_invalid_user(self):    
        response = self.client.post(
            reverse("user-update", kwargs={'pk':100}),
            data=json.dumps(self.valid_user_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_data_user(self):    
        response = self.client.post(
            reverse("user-update", kwargs={'pk':self.staticUser.pk}),
            data=json.dumps(self.invalid_user_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #Test user delete
    def test_delete_user(self):
        response = self.client.delete(
            reverse("user-delete", kwargs={'pk':self.staticUser.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    #Test invalid User delete
    def test_delete_invalid_user(self):
        response = client.delete(
            reverse("user-delete", kwargs={'pk':100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""Tests For Product Views"""
class ProductTestCase(APITestCase):
    
    def setUp(self):
        self.test_product = Product.objects.create(
            name="android",image="google.com",category="phones",
            stock="126", price="5000", score="4.5",click_count="12303",
            description="lorem ipsum"
        )
        Product.objects.create(
            name="android",image="google.com",category="phones",
            stock="126", price="5000", score="4.5",click_count="12303",
            description="lorem ipsum"
        )
        self.valid_product={
            "name":"Iphone","image":"Apple.com","category":"phones",
            "stock":"1245","price":"7900","score":"4.2","click_count":"4521",
            "description":"lorem ipsum"
        }
        self.invalid_product={
            "name":"","image":"","category":"",
            "stock":"","price":"7900","score":"4.2","click_count":"4521",
            "description":"lorem ipsum"
        }
        self.valid_product_update={
            "name":"Iphone(updated)","image":"Apple.com","category":"phones",
            "stock":"1212","price":"7999","score":"4.2","click_count":"4521",
            "description":"lorem ipsum"
        }
        self.invalid_product_update={
            "name":"","image":"","category":"",
            "stock":"","price":"","score":"","click_count":"",
            "description":""
        }
    
    #Test for getting all products
    def test_get_all_products(self):
        response = self.client.get(reverse('product-list'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #Test validity of Product's detail
    def test_get_valid_product(self):
        response = self.client.get(
            reverse('product-detail', kwargs={'pk':self.test_product.pk}))
        product = Product.objects.get(pk=self.test_product.pk)
        serializer = ProductSerializer(product)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_product(self):
        response = self.client.get(
            reverse('product-detail', kwargs={'pk':100}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #Test for Product creation 
    def test_create_valid_product(self):
        response = self.client.post(
            reverse('product-create'),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):        
        response = self.client.post(
            reverse('product-create'),
            data=json.dumps(self.invalid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    #Test for product Update and Delete
    def test_update_product(self):
        response = self.client.post(
            reverse('product-update',kwargs={'pk':self.test_product.pk}),
            data=json.dumps(self.valid_product_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_invalid_product(self):
        response = self.client.post(
            reverse('product-update',kwargs={'pk':100}),
            data=json.dumps(self.valid_product_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_data_product(self):
        response = self.client.post(
            reverse('product-update',kwargs={'pk':self.test_product.pk}),
            data=json.dumps(self.invalid_product_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_product(self):
        response=self.client.delete(
            reverse('product-delete',kwargs={'pk':self.test_product.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_invalid_product(self):
        response=self.client.delete(
            reverse('product-delete',kwargs={'pk':100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)