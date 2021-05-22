from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #User api urls
    path('user-list/', views.UserList, name='user-list'),
    path('user-detail/<int:pk>/', views.UserDetail, name='user-detail'),
    path('user-create/', views.UserCreate, name='user-create'),
    path('user-update/<int:pk>/', views.UserUpdate, name='user-update'),
    path('user-delete/<int:pk>/', views.UserDelete, name='user-delete'),
    path('user-login/', views.UserLogin, name='user-login'),
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
    path('cart-details/<int:pk>/', views.UserCart, name='cart-details'),
]