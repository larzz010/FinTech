from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if email is None:
            raise ValueError('The Email field must be set for superuser.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True, default='')
    email = models.EmailField(unique=True)
    coins = models.ManyToManyField('Coin', through='UserCoin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class CustomCoinManager(models.Manager):
    def create_coin(self, coin_name, coin_value, **extra_fields):
        if not coin_name:
            raise ValueError("The coin field must be set")

        coin = self.model(coin_name=coin_name, coin_value=coin_value, **extra_fields)
        coin.save()
        return coin


class Coin(models.Model):
    coin_name = models.CharField(max_length=100)
    coin_value = models.DecimalField(max_digits=100, decimal_places=2)
    users = models.ManyToManyField('CustomUser', through='UserCoin')

    objects = CustomCoinManager()

    def __str__(self):
        return self.coin_name


class UserCoinManager(models.Manager):
    pass


class UserCoin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    coin_quantity = models.DecimalField(max_digits=20, decimal_places=1, default=0)
    objects = UserCoinManager()


class Transactions(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='Sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='Receiver', on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save_transaction(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_sender_receiver_quantity()

    def update_sender_receiver_quantity(self):
        sender_user_coin = UserCoin.objects.get(user=self.sender, coin=self.coin)
        receiver_user_coin = UserCoin.objects.get(user=self.receiver, coin=self.coin)

        sender_user_coin.quantity -= self.amount
        receiver_user_coin.quantity += self.amount

        sender_user_coin.save()
        receiver_user_coin.save()
