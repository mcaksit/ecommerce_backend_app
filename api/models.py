from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
    ('ProductManager', 'ProductManager'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    #role = models.CharField(choices=ROLE_CHOICES, max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.CharField(max_length=255)
    stock = models.IntegerField(default=0, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    description = models.TextField(blank=True, null=True)
    purchase_count = models.IntegerField(default=0, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_initialized = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.transaction_id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)


class Order_v2(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True)
    date_ordered = models.DateTimeField(default=timezone.now)
    Status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.transaction_id)


class OrderItem_v2(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order_v2, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(null=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order_v2, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    full_address = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_address