import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Customer, Product
from ..serializers import CustomerSerializer, ProductSerializer


#Models testing
class UrlTests(TestCase):

    def test_api_overview(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
