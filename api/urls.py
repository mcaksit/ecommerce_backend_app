from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #User api urls
    path('user-login/', views.TokenLogin.as_view()),
    path('user-logout/', views.TokenLogout.as_view()),
    path('user-create/', views.UserCreate, name='user-create'),
    path('user-update/<int:pk>/', views.UserUpdate.as_view()),
    path('user-detail/<int:pk>/', views.UserDetail.as_view()),
    path('user-delete/<int:pk>/', views.UserDelete.as_view()),
    path('user-checkout/<int:pk>/', views.UserCheckout.as_view()),
    #Customer api urls
    path('customer-list/', views.CustomerList.as_view()),
    path('customer-detail/<int:pk>/', views.CustomerDetail.as_view()),
    path('customer-create/', views.CustomerCreate, name='customer-create'),
    path('customer-update/<int:pk>/', views.CustomerUpdate, name='customer-update'),
    path('customer-delete/<int:pk>/', views.CustomerDelete, name='customer-delete'),
    # path('user-login/', views.CustomerLogin, name='user-login'),
    #Product api urls
    path('product/search=<str:category>/<str:param>/',views.ProductCategoricalSearch, name='product-categorical-search'),
    path('product/search=<str:param>/',views.ProductSearch, name='product-search'),
    path('product-list/', views.ProductList, name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetail, name='product-detail'),
    path('product-create/', views.ProductCreate.as_view()),
    path('product-update/<int:pk>/', views.ProductUpdate.as_view()),
    path('product-delete/<int:pk>/', views.ProductDelete.as_view()),
    path('product-reviews/<int:pk>/', views.ListReviews, name='product-reviews'),
    #Review api urls
    path('make-review/', views.MakeReview.as_view()),
    #Product api urls (Alternative)
    path('list-products/', views.ProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetails.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    #Cart api urls
    path('view-cart/<int:pk>/', views.CustomerCart2.as_view()),
    path('view-cart-products/<int:pk>/', views.CustomerCart.as_view()),
    path('add-to-cart/', views.AddToCart.as_view()),
    path('remove-from-cart/', views.RemoveFromCart.as_view()),
]