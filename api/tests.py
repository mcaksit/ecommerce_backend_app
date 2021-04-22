import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Customer, Product
from api.serializers import CustomerSerializer, ProductSerializer


# Create your tests here.
class UrlTests(TestCase):

    def test_api_overview(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

class CustomerAPITestCase(APITestCase):
    
    def setUp(self):
        self.valid_customer = {
            "name":"testname",
            "surname":"testsurname",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }
        self.invalid_customer = {
            "name":"",
            "surname":"",
            "phone":"111111",
            "email":"testemail@localhost.app"
        }


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
    