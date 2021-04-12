from django.db import models
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    stock = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    score = models.CharField(max_length=5)
    click_count = models.CharField(max_length=30)

    def __str__(self):
        return self.name