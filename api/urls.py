from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #User api urls
    path('user-list/', views.UserList, name='user-list'),
    path('user-detail/<str:pk>/', views.UserDetail, name='user-detail'),
    path('user-create/', views.UserCreate, name='user-create'),
    path('user-update/<str:pk>/', views.UserUpdate, name='user-update'),
    path('user-delete/<str:pk>/', views.UserDelete, name='user-delete'),
    #Product api urls
    path('search/<str:param>/',views.ProductSearch, name='product-search'),
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<str:pk>/', views.ProductDetail, name='product-detail'),
    path('product-create/', views.ProductCreate, name='product-create'),
    path('product-update/<str:pk>/', views.ProductUpdate, name='product-update'),
    path('product-delete/<str:pk>/', views.ProductDelete, name='product-delete'),

]