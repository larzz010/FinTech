from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buy-coins/', views.buy_coins, name='buy_coins'),
    path('add_coins/', views.add_coin, name='add_coin'),
]
