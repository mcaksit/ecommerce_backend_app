from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('customer-list/', views.CustomerList, name='customer-list'),
    path('customer-detail/<str:pk>/', views.CustomerDetail, name='customer-detail'),
    path('customer-create/', views.CustomerCreate, name='customer-create'),
    path('customer-update/<str:pk>/', views.CustomerUpdate, name='customer-update'),
    path('customer-delete/<str:pk>/', views.CustomerDelete, name='customer-delete'),
    
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<str:pk>/', views.ProductDetail, name='product-detail')
]