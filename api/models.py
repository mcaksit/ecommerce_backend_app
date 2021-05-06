from django.db import models
from django.utils import timezone

# Create your models here.

ROLE_CHOICES = (
    'Standard',
    'Admin',
)

CATEGORY_CHOICES = (
    'Smartphone',
    'Computer',
    'TV',
    'Tablet',
)

class User(models.Model):
    role = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    stock = models.CharField(max_length=20)
    price = models.IntegerField()
    score = models.CharField(max_length=5)
    click_count = models.CharField(max_length=30)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name