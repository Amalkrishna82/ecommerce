"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
app_name="shop"
urlpatterns = [
    path('', views.CategoryView.as_view(), name='categories'),
    path('product/<int:i>',views.ProductView.as_view(),name='product'),
    path('productdetail/<int:i>',views.ProductDetail.as_view(),name='productdetail'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Userlogin.as_view(), name='login'),
    path('logout', views.Userlogout.as_view(), name='logout'),
    path('addproduct', views.AddProduct.as_view(), name='addproduct'),
    path('addcategory', views.AddCategory.as_view(), name='addcategory'),
    path('addstock/<int:i>', views.AddStock.as_view(), name='addstock'),
    path('addstock/<int:i>', views.AddStock.as_view(), name='addstock'),
    path('search/', views.SearchView.as_view(), name='search'),
]
