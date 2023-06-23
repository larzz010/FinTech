from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buy-coins/', views.buy_coins, name='buy_coins'),
    path('add_coins/', views.add_coin, name='add_coin'),
    path('add_food_drink_item/', views.add_food_drink_item, name='add_food_drink_item'),
    path('create_pending_transaction/', views.create_pending_transaction, name='create_pending_transaction'),
    path('approve_pending_transactions/', views.approve_pending_transactions, name='approve_pending_transactions')
]
