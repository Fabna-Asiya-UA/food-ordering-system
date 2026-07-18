from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_list, name='food_list'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-food/', views.add_food, name='add_food'),
    path('edit-food/<int:pk>/', views.edit_food, name='edit_food'),
    path('delete-food/<int:pk>/', views.delete_food, name='delete_food'),

    path('cart/add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),

    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]