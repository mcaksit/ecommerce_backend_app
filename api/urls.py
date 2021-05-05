from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #User api urls
    path('customer-list/', views.CustomerList, name='customer-list'),
    path('customer-detail/<str:pk>/', views.CustomerDetail, name='customer-detail'),
    path('customer-create/', views.CustomerCreate, name='customer-create'),
    path('customer-update/<str:pk>/', views.CustomerUpdate, name='customer-update'),
    path('customer-delete/<str:pk>/', views.CustomerDelete, name='customer-delete'),
    #Product api urls
    path('product/search=<str:category>/<str:param>/',views.ProductCategoricalSearch, name='product-categorical-search'),
    path('product/search=<str:param>/',views.ProductSearch, name='product-search'),
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<str:pk>/', views.ProductDetail, name='product-detail'),
    path('product-create/', views.ProductCreate, name='product-create'),
    path('product-update/<str:pk>/', views.ProductUpdate, name='product-update'),
    path('product-delete/<str:pk>/', views.ProductDelete, name='product-delete'),

]