
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from .forms import RegistrationForm, LoginForm, CoinForm, FoodDrinkItemForm, PendingTransactionForm, ItemForm
from .models import UserCoin, Coin, CustomUser, FoodDrinkItem, PendingTransaction, PendingTransactionItem, Transactions
from decimal import Decimal
from django.forms import formset_factory
from django.db.models import F


# Code that manages the registrations
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


# Code that manages the login of the app
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


# Code that shows the dashboard of the app
@login_required(login_url='login/')
def dashboard(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('login')
    owned_coins = UserCoin.objects.filter(user=request.user)
    return render(request, 'FinApp/dashboard.html', {'owned_coins': owned_coins})


# This code is used so users can buy coins
@login_required
def buy_coins(request):
    if request.method == 'POST':
        coin_name = request.POST.get('coin_name')
        quantity = request.POST.get('quantity')

        try:
            coin = Coin.objects.get(coin_name=coin_name)
        except Coin.DoesNotExist:
            return render(request, 'FinApp/buy_coins.html', {'message': 'Invalid coin selection.'})

        quantity = Decimal(quantity)
        total_price = coin.coin_value * quantity

        user_coin, created = UserCoin.objects.get_or_create(user=request.user, coin=coin)
        if created:
            user_coin.coin_quantity = quantity
        else:
            user_coin.coin_quantity = F('coin_quantity') + quantity
        user_coin.save()

        return redirect('dashboard')

    coins = Coin.objects.all()
    return render(request, 'FinApp/buy_coins.html', {'coins': coins})


# This code is used to add coins by vendors
@login_required
def add_coin(request):
    if not request.user.is_vendor:
        return render(request, 'error.html', {'message': 'Only vendors can access this page.'})

    if request.method == 'POST':
        form = CoinForm(request.POST)
        if form.is_valid():
            coin = form.save()
            UserCoin.objects.create(user=request.user, coin=coin, coin_quantity=0)
            return redirect('dashboard')
    else:
        form = CoinForm()

    return render(request, 'FinApp/add_coins.html', {'form': form})


# Code used to add food and drinks to the menu for vendors.
@login_required
def add_food_drink_item(request):
    if not request.user.is_vendor:
        return render(request, 'FinApp/dashboard.html', {})

    vendor = request.user

    if request.method == 'POST':
        form = FoodDrinkItemForm(request.POST)
        if form.is_valid():
            food_drink_item = form.save(commit=False)
            food_drink_item.vendor = vendor
            food_drink_item.save()
            return redirect('dashboard')
    else:
        form = FoodDrinkItemForm()

    return render(request, 'FinApp/add_food_drink_item.html', {'form': form})


# Code used to create pending_transactions
@login_required
def create_pending_transaction(request):
    ItemFormSet = formset_factory(ItemForm, extra=1)

    if request.method == 'POST':
        form = PendingTransactionForm(request.POST)
        formset = ItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            user = form.cleaned_data['user']
            vendor = request.user
            for item_form in formset:
                item_id = item_form.cleaned_data['item']
                item = get_object_or_404(FoodDrinkItem, name=item_id)
                coin_id = item.coin
                quantity = item_form.cleaned_data['quantity']
                price = item.price
                total_price = quantity * price
                pending_transaction = PendingTransaction.objects.create(vendor=vendor, user=user, coin=coin_id, amount=total_price  )

            for item_form in formset:
                item = item_form.cleaned_data['item']
                quantity = item_form.cleaned_data['quantity']
                price = item.price
                total_price = quantity * price
                PendingTransactionItem.objects.create(transaction=pending_transaction, food_drink_item=item,
                                                      quantity=quantity, coin=item.coin, total_price=total_price)

            return redirect('dashboard')
    else:
        form = PendingTransactionForm()
        formset = ItemFormSet()

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'FinApp/create_pending_transaction.html', context)


#Code used to approve pending_transactions
@login_required()
def approve_pending_transactions(request):
    pending_transactions = PendingTransaction.objects.filter(user=request.user)

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        pending_transaction = get_object_or_404(PendingTransaction, id=transaction_id)

        vendor = pending_transaction.vendor
        coin = pending_transaction.coin
        total_coins_used = pending_transaction.amount
        user_coin = get_object_or_404(UserCoin, user=request.user, coin=coin)
        vendor_coin = get_object_or_404(UserCoin, user=vendor, coin=coin)

        if user_coin is None:
            return messages.error(request, 'No coins found.')

        if user_coin.coin_quantity < total_coins_used:
            return messages.error(request, 'Insufficient number of coins.')

        user_coin.coin_quantity -= total_coins_used
        user_coin.save()
        vendor_coin.coin_quantity += total_coins_used
        vendor_coin.save()

        return redirect('dashboard')

    context = {
        'pending_transactions': pending_transactions,
    }
    return render(request, 'FinApp/approve_pending_transactions.html', context)
