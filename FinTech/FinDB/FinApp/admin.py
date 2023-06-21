from django.contrib import admin
from .models import CustomUser, Coin, UserCoin

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Coin)
admin.site.register(UserCoin)
