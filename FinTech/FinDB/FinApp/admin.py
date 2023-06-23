from django.contrib import admin
from .models import CustomUser, Coin, UserCoin, Transactions, FoodDrinkItem, PendingTransaction, PendingTransactionItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Coin)
admin.site.register(UserCoin)
admin.site.register(Transactions)
admin.site.register(PendingTransaction)
admin.site.register(FoodDrinkItem)
admin.site.register(PendingTransactionItem)
