from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    
    path('products/', views.product_list, name='product_list'),
    
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    path('signup/', views.signup, name='signup'),

    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
]