from django import forms
from .models import CustomUser, Coin, FoodDrinkItem
from django.forms import formset_factory


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CoinForm(forms.ModelForm):
    coin_name = forms.CharField(max_length=20)
    coin_value = forms.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        model = Coin
        fields = ['coin_name', 'coin_value']


class FoodDrinkItemForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        model = FoodDrinkItem
        fields = ['name', 'price', 'coin']


class ItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=FoodDrinkItem.objects.all())
    quantity = forms.IntegerField(min_value=1)


class PendingTransactionForm(forms.Form):
    items = formset_factory(ItemForm, extra=1)
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
