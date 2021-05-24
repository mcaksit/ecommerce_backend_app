from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #Customer api urls
    path('customer-list/', views.CustomerList, name='customer-list'),
    path('customer-detail/<int:pk>/', views.CustomerDetail, name='customer-detail'),
    path('customer-create/', views.CustomerCreate, name='customer-create'),
    path('customer-update/<int:pk>/', views.CustomerUpdate, name='customer-update'),
    path('customer-delete/<int:pk>/', views.CustomerDelete, name='customer-delete'),
    path('user-login/', views.CustomerLogin, name='user-login'),
    #Product api urls
    path('product/search=<str:category>/<str:param>/',views.ProductCategoricalSearch, name='product-categorical-search'),
    path('product/search=<str:param>/',views.ProductSearch, name='product-search'),
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetail, name='product-detail'),
    path('product-create/', views.ProductCreate, name='product-create'),
    path('product-update/<int:pk>/', views.ProductUpdate, name='product-update'),
    path('product-delete/<int:pk>/', views.ProductDelete, name='product-delete'),
    #Product api urls (Alternative)
    path('list-products/', views.ProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetails.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    #Cart api urls
]