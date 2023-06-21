
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from .forms import RegistrationForm, LoginForm, CoinForm
from .models import UserCoin, Coin
from decimal import Decimal
import time


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'FinApp/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
        next_url = request.GET.get('next')
        if next_url:
            form.initial['next'] = next_url
        else:
            messages.error(request, 'You need to log in.')

    return render(request, 'FinApp/login.html', {'form': form})


def home(request):
    return render(request, 'FinApp/index.html')


@login_required(login_url='login/')
def dashboard(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('login')
    owned_coins = UserCoin.objects.filter(user=request.user)
    return render(request, 'FinApp/dashboard.html', {'owned_coins': owned_coins})


@login_required
def buy_coins(request):
    if request.method == 'POST':
        coin_name = request.POST.get('coin_name')
        quantity = request.POST.get('quantity')

        try:
            coin = Coin.objects.get(coin_name=coin_name)
        except Coin.DoesNotExist:
            return render(request, 'FinApp/buy_coins.html', {'message': 'Invalid coin selection.'})

        # Calculate the total price
        quantity = Decimal(quantity)
        total_price = coin.coin_value * quantity

        # Perform necessary operations for buying coins
        # Validate inputs, update user's coin balance, etc.

        # Create a UserCoin entry for the user
        user_coin = UserCoin(user=request.user, coin=coin, coin_quantity=quantity)
        user_coin.save()

        # Redirect to a success page or display a success message
        return redirect('dashboard')

    coins = Coin.objects.all()
    return render(request, 'FinApp/buy_coins.html', {'coins': coins})


@login_required
def add_coin(request):
    if not request.user.is_vendor:
        return render(request, 'error.html', {'message': 'Only vendors can access this page.'})

    if request.method == 'POST':
        form = CoinForm(request.POST)
        if form.is_valid():
            coin = form.save()
            return redirect('dashboard')
    else:
        form = CoinForm()

    return render(request, 'FinApp/add_coins.html', {'form': form})
