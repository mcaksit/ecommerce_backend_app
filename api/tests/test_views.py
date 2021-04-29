import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Customer, Product
from ..serializers import CustomerSerializer, ProductSerializer


#Initialize client
client = Client()
"""Test For Customer Views"""
class CustomerTestCase(APITestCase):

    def setUp(self):
        self.staticCustomer = Customer.objects.create(
            name="staticname",surname="staticsurname",phone="1234",email="static@test.com"
        )
        Customer.objects.create(
            name="person",surname="persurname",phone="12324",email="stpersonc@test.com"
        )
        self.valid_customer = {
            "name":"testname",
            "surname":"testsurname",
            "password":"1234",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.invalid_customer = {
            "name":"",
            "surname":"",
            "password":"",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.valid_customer_update = {
            "name":"testname(updated)",
            "surname":"testsurname",
            "password":"nani",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.invalid_customer_update = {
            "name":"",
            "surname":"",
            "phone":"",
            "email":""
        }
    #Test get all Customers' details
    def test_get_all_customer(self):
        response = self.client.get(reverse("customer-list"))
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    #Test valid Customer's detail 
    def test_get_valid_customer(self):
        response = self.client.get(
            reverse("customer-detail", kwargs={'pk':self.staticCustomer.pk}))
        customer = Customer.objects.get(pk=self.staticCustomer.pk)
        serializer = CustomerSerializer(customer)

        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test invalid Customer's detail
    def test_get_invalid_customer(self):
        response = self.client.get(
            reverse("customer-detail", kwargs={'pk':100}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #Test Customer create
    def test_create_customer(self):
        response = self.client.post(
            reverse("customer-create"), 
            data=json.dumps(self.valid_customer),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_customer(self):
        response = self.client.post(
            reverse("customer-create"),
            data=json.dumps(self.invalid_customer),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    #Test customer update
    def test_update_customer(self):
        response = self.client.post(
            reverse("customer-update", kwargs={'pk':self.staticCustomer.pk}),
            data=json.dumps(self.valid_customer_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    #Test invalid updates wrong id/empty data
    def test_update_invalid_customer(self):    
        response = self.client.post(
            reverse("customer-update", kwargs={'pk':100}),
            data=json.dumps(self.valid_customer_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_data_customer(self):    
        response = self.client.post(
            reverse("customer-update", kwargs={'pk':self.staticCustomer.pk}),
            data=json.dumps(self.invalid_customer_update),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #Test customer delete
    def test_delete_customer(self):
        response = self.client.delete(
            reverse("customer-delete", kwargs={'pk':self.staticCustomer.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    #Test invalid Customer delete
    def test_delete_invalid_customer(self):
        response = client.delete(
            reverse("customer-delete", kwargs={'pk':100}))
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