from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.index, name='index'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Products
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),

    # Orders
    path('track/<int:order_id>/', views.track_order, name='track_order'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Extra Pages
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]