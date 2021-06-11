from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import login as django_login, logout as django_logout
from django import template

import datetime
from django.template.loader import render_to_string
#from weasyprint import HTML
import tempfile

from .models import *
from .serializers import *


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'User Login':'user-login/',
        'User Logout':'user-logout/',
        'User Create':'user-create/',
        'User Update':'user-update/<str:pk>/',
        'User Details':'user-detail/<str:pk>/',
        'User Delete':'user-delete/<str:pk>/',
        'User Checkout':'user-checkout/<int:pk>/',
        # 'Token Get':'get-token/ ("api/" yok basında)',
        'Customer List':'customer-list/',
        'Customer Create':'customer-create/',
        'Customer Update':'customer-update/<str:pk>/',
        'Customer Details':'customer-detail/<str:pk>/',
        'Customer Details':'customer-detail/<str:pk>/',
        'Customer Delete':'customer-delete/<str:pk>/',
        'Product List':'product-list/',
        'Product Search':'product/?search=<param>',
        'Product Details':'product-detail/<str:pk>/',
        'Product Create':'product-create/',
        'Product Update':'product-update/<str:pk>/',
        'Product Delete':'product-delete/<str:pk>/',
        'Product Reviews':'product-reviews/<int:pk>/',
        'Create/Update a Review':'make-review/',
        '!(Alternative) Products list':'list-products/',
        '!(Alternative) Products By Categories':'products/<slug:category_slug>/',
        '!(Alternative) Product Details':'products/<slug:category_slug>/<slug:product_slug>/',
        'Cart Details':'view-cart/<int:pk>/',
        'Cart Products':'view-cart-products/<int:pk>/',
        'Add To Cart':'add-to-cart/',
        'Remove From Cart':'remove-from-cart/',
        #'Export Invoices as Downloadable PDF File':'export-pdf/<str:range>/',
        'Create Discount':'create-discount/',
        'List Orders':'order-list/',
        'Update Order':'order-update/<int:pk>/',
        'Approve Review':'review-approval/<int:pk>/',
    }
    return Response(api_urls)


class TokenLogin(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return_user = UserSerializer(user)
        return Response({"token": token.key, "user": return_user.data}, status=status.HTTP_200_OK)


class TokenLogout(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class UserDetail(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     permission_required = 'api.add_cart'
class UserDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if (request.user != user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# class CustomerList(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     permission_required = 'api.delete_cart'
class CustomerList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class CustomerDetail(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     permission_required = 'api.add_cart'
class CustomerDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #Get Customer detail
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

       
#Create customer
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def CustomerCreate(request):
    serializer = CustomerSerializerUpdate(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Create customer
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def UserCreate(request):

    if ((not(request.data.get('name')) or request.data.get('name') == "")
        or (not(request.data.get('password')) or request.data.get('password') == "")
        or (not(request.data.get('email')) or request.data.get('email') == "")
        or (not(request.data.get('phone')) or request.data.get('phone') == "")):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        customersGroup = Group.objects.get(name='Customer')
        createdUser = User.objects.create(username=request.data.get('name'), password=request.data.get('password'), email=request.data.get('email'))
        createdUser.set_password(request.data.get('password'))
        customersGroup.user_set.add(createdUser)

        Customer.objects.create(name=request.data.get('name'), phone=request.data.get('phone'), email=request.data.get('email'), user=createdUser)
        serializer = UserSerializer(createdUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except :
        return Response(status=status.HTTP_400_BAD_REQUEST)


#Customer Login
# @api_view(['POST'])
# def CustomerLogin(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         customer_qs = Customer.objects.get(email=email)
#     except Customer.DoesNotExist:
#         return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)    

#     if password == customer_qs.password:
#         serializer = CustomerSerializerUpdate(customer_qs)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response("Entered wrong password!", status=status.HTTP_404_NOT_FOUND)
    

#Update a customer
@api_view(['POST'])
#@authentication_classes([authentication.SessionAuthentication])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def CustomerUpdate(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializerUpdate(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserUpdate(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.add_cart'
class UserUpdate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if (request.user != user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            customer = Customer.objects.get(user=user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            if (request.data.get('name') and request.data.get('name') != ""):
                user.username = request.data.get('name')
                customer.name = request.data.get('name')
            if (request.data.get('password') and request.data.get('password') != ""):
                user.set_password(request.data.get('password'))
            if (request.data.get('email') and request.data.get('email') != ""):
                user.email = request.data.get('email')
                customer.email = request.data.get('email')
            if (request.data.get('phone') and request.data.get('phone') != ""):
                customer.phone = request.data.get('phone')

            user.save()
            customer.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)


#Delete a customer
@api_view(['DELETE'])
#@authentication_classes([authentication.SessionAuthentication])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def CustomerDelete(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    customer.delete()    
    return Response(status=status.HTTP_204_NO_CONTENT)


# class UserDelete(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.add_cart'
class UserDelete(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if (request.user != user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        user.delete()    
        return Response(status=status.HTTP_204_NO_CONTENT)


#Product APIs
#Product search
@api_view(['GET'])
def ProductSearch(request, param):
    try:
        product = Product.objects.filter(name__icontains=param)
        
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Product search based on category
@api_view(['GET'])
def ProductCategoricalSearch(request, category, param):
    try:
        product = Product.objects.filter(category=category).filter(name__icontains=param)
        #product = first_qs.objects.filter(name__icontains=param)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

        
@api_view(['GET'])
def ProductList(request):    
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ProductDetail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class ProductCreate(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.change_cart'
class ProductCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializerUpdate(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# class ProductUpdate(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.change_cart'
class ProductUpdate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializerUpdate(instance=product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# class ProductDelete(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.change_cart'
class ProductDelete(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetails(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404
    

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        

class CustomerCart2(APIView):
    authentication_classes = [authentication.TokenAuthentication] #authentication.TokenAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Cart.objects.get(id=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class CustomerCart(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     permission_required = 'api.add_cart'
class CustomerCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if (request.user != user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            cart, created = Cart.objects.get_or_create(customer=user.customer)
            cartItems = CartItem.objects.filter(cart=cart.id)

            items = []
            cost = 0

            for i in range(len(cartItems)):
                item = Product.objects.get(id=str(cartItems[i].product.id))
                items.append(item)
                cost += item.price * cartItems[i].quantity

        except User.DoesNotExist:
            items = []

        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class AddToCart(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.add_cart'
class AddToCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        cartItem = request.data.get('cartItem')

        try:
            user_qs = User.objects.get(id=user_id)
            if (request.user != user_qs):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response("User does not exist!", status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(customer=user_qs.customer)
        
        try:
            product = Product.objects.get(id=cartItem.get("product"))
        except Product.DoesNotExist:
            return Response("Product does not exist!", status=status.HTTP_404_NOT_FOUND) 


        serializer = CartItemSerializer(data=cartItem)

        if serializer.is_valid():
            product = Product.objects.get(id=cartItem.get("product"))
            cartItem2, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': serializer.data.get("quantity")})
            if (created == False):
                cartItem2.quantity = cartItem2.quantity + serializer.data.get("quantity")
                
            if (product.stock - cartItem.get("quantity") >= 0):
                product.stock = product.stock - cartItem.get("quantity")
                product.save()
                cartItem2.save()
            else :
                return Response("Product is out of stock or stock exceeded!", status=status.HTTP_400_BAD_REQUEST)
            
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RemoveFromCart(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.add_cart'
class RemoveFromCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        cartItem_id = request.data.get('cartItem_id')

        try:
            user_qs = User.objects.get(id=user_id)
            if (request.user != user_qs):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response("User does not exist!", status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(customer=user_qs.customer)
        cartItems = CartItem.objects.filter(cart=cart.id)
        
        try:
            cartItem = cartItems.get(id=cartItem_id)
        except CartItem.DoesNotExist:
            return Response("Item does not exist!", status=status.HTTP_404_NOT_FOUND) 

        product = cartItem.product
        product.stock = product.stock + cartItem.quantity
        product.save()
        cartItem.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ListReviews(request, pk):
    try:
        reviews = Review.objects.filter(product=pk)        
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class MakeReview(PermissionRequiredMixin, APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_required = 'api.add_cart'
class MakeReview(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            prod_id = request.data.get("product_id")
            user_id = request.data.get("user_id")
            user = User.objects.get(id=user_id)
            
            if (request.user != user):
               return Response(status=status.HTTP_401_UNAUTHORIZED)

            prod = Product.objects.get(id=prod_id)
            
            review, created = Review.objects.get_or_create(customer=user.customer, product=prod, defaults={'comment': request.data.get("comment"), 'stars': request.data.get("stars")})
            review.comment = request.data.get("comment")
            review.stars = request.data.get("stars")
            review.approval_status = False           
            review.save()
            
            revs = Review.objects.filter(product=prod_id)
            score_sum = 0
            score_count = 0
            for i in range(len(revs)):
                if revs[i].stars:
                    score_sum += revs[i].stars
                    score_count += 1
            prod.score = score_sum / score_count
            prod.save()

            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserCheckout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if (request.user != user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(customer=Customer.objects.get(user=user))

        order = Order_v2.objects.create(customer=cart.customer, transaction_id=cart.transaction_id, Status="Processing")

        shippingAddress = ShippingAddress.objects.create(customer=order.customer, order=order, city=request.data.get("city"),
        district=request.data.get("district"), full_address=request.data.get("full_address"))

        cartItems = CartItem.objects.filter(cart=cart)
        for i in range(len(cartItems)):
            orderItem = OrderItem_v2.objects.create(product=cartItems[i].product,
             order=order, quantity=cartItems[i].quantity, date_added=cartItems[i].date_added)

        for i in range(len(cartItems)):
            cartItems[i].delete()

        return Response(status=status.HTTP_200_OK)

class ExportPDF(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  

    def get(self,request,range):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Invoices'+ str(datetime.datetime.now())+'.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        dates= range.split(':')
        
        orders=Order_v2.objects.filter(date_ordered__range=[dates[0], dates[1]])
        items=OrderItem_v2.objects.filter(date_added__range=[dates[0], dates[1]])
        address=ShippingAddress.objects.all()

        pricesums=[]
        for order in orders:
            price_sum=0
            for item in items:
                if item.order == order:
                    price_sum = price_sum + (item.quantity*item.product.price) 
            pricesums.append((order,price_sum))
        print(pricesums)
        
        html_string = render_to_string('new-testing.html',{'orders':pricesums,'items':items, 'address':address,'dates':dates})
        html=HTML(string=html_string)
        
        result=html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()        
            output.seek(0)
            response.write(output.read())
        
        return response

class CreateDiscount(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  

    def post(self, request):
        try:
            product_ids = request.data.get("product_id")
            discount_amount = request.data.get("discount")    
            for prod_id in product_ids:
                product = Product.objects.get(id=prod_id)
                product.price = (product.price * (100-discount_amount)) / 100 
                product.save() 
            
            return Response(status=status.HTTP_200_OK)     
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  

    def get(self, request):
        try:
            orders = Order_v2.objects.filter(Status="Processing")
        except Order_v2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class OrderCheckout(APIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]  

#     def get(self, request, pk):
#         try:
#             orders = Order_v2.objects.get(id=pk)
#             order_item.Status= "Processing"
#             order_item.save()

#         except Order_v2.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         return Response(status=status.HTTP_200_OK)


#Update order to become completed
class OrderUpdate(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    
    def get(self, request, pk):
        try:
            order_item = Order_v2.objects.get(id=pk)
            order_item.Status= "Delivered"
            order_item.save()
        except Order_v2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

#Delete review if not approved 
class ApproveReview(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  

    def get(self,request,pk):
        try:
            review_item = Review.objects.get(id=pk)
            review_item.delete()            
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

class MakeRefund(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  

    def get(self,request,pk):
        try:
            order_item = Order_v2.Objects.get(id=pk)
            order_item.Status = "Refunded"
            order_item.save()
        except Order_v2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

class RequestRefund(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,pk):
        try:
            order_item = Order_v2.Objects.get(id=pk)
            if(datetime.datetime.now()-order_item.date_added() > datetime.timedelta(days=30)):                    
                if(order_item.Status == "Completed"):
                    order_item.Status = "Customer requests refund"
                    order_item.save()
                else:
                    return Response("Item Cannot be refunded",status=status.HTTP_400_BAD_REQUEST)
        except Order_v2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #return Response(status=status.HTTP_200_OK)

#class 
