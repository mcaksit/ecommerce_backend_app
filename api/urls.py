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
    path('product-reviews/<int:pk>/', views.ListReviews, name='product-reviews'),
    #Review api urls
    path('make-review/', views.MakeReview, name='make-review'),
    #path('product-reviews/<int:pk>/', views.ListReviews, name='product-reviews'),
    #Product api urls (Alternative)
    path('list-products/', views.ProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetails.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    #Cart api urls
    path('view-cart/<int:pk>/', views.CustomerCart2.as_view()),
    path('view-cart-products/<int:pk>/', views.CustomerCart, name='customer-cart'),
    path('add-to-cart/', views.AddToCart, name='add-to-cart'),
    path('remove-from-cart/', views.RemoveFromCart, name='remove-from-cart'),
]