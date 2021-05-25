from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
    ('ProductManager', 'ProductManager'),
)


# def django_sub_dict(obj):
#     allowed_fields = obj.allowed_fields() # pick the list containing the requested fields
#     sub_dict = {}
#     for field in obj._meta.fields: # go through all the fields of the model (obj)
#         if field.name in allowed_fields: # be sure to only pick fields requested
#             if field.is_relation: # will result in true if it's a foreign key
#                 sub_dict[field.name] = django_sub_dict(
#                     getattr(obj, field.name)) # call this function, with a new object, the model which is being referred to by the foreign key.
#             else: # not a foreign key? Just include the value (e.g., float, integer, string)
#                 sub_dict[field.name] = getattr(obj, field.name)
#     return sub_dict # returns the dict generated


# class ProductManager(models.Manager):
#     def get_by_natural_key(self, name, image, price, category, score):
#         return self.get(name=name, image=image, price=price, category=category, score=score)


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
        #return "{" + "name:{0} , image:{1} , price:{2} , category:{3} , score:{4}".format(self.name, self.image, self.price, self.category, self.score) + "}"
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    # def allowed_fields(self):
    #     return [
    #             'name',
    #             'image',
    #             'price',
    #             'category',
    #             'score',
    #             ]

    # def natural_key(self):
    #     return django_sub_dict(self)

    # def natural_key(self):
    #     return (self.name, self.image, self.price, self.category, self.score)


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
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, related_name='cartItems', on_delete=models.CASCADE, null=True, blank=True)
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