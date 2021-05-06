from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #User api urls
    path('user-list/', views.UserList, name='user-list'),
    path('user-detail/<int:pk>/', views.UserDetail, name='user-detail'),
    path('user-create/', views.UserCreate, name='user-create'),
    path('user-update/<int:pk>/', views.UserUpdate, name='user-update'),
    path('user-delete/<int:pk>/', views.UserDelete, name='user-delete'),
    #Product api urls
    path('product/search=<str:category>/<str:param>/',views.ProductCategoricalSearch, name='product-categorical-search'),
    path('product/search=<str:param>/',views.ProductSearch, name='product-search'),
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetail, name='product-detail'),
    path('product-create/', views.ProductCreate, name='product-create'),
    path('product-update/<int:pk>/', views.ProductUpdate, name='product-update'),
    path('product-delete/<int:pk>/', views.ProductDelete, name='product-delete'),

]