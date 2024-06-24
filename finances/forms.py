from django import forms
from django.contrib.auth.forms import UserChangeForm

from users.models import User, Wallet
from finances.models import Transaction


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя пользователя'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'True',
        'id': 'readonly'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'example@gmail.com'
    }))

    class Meta:
        model = User
        fields = (
            'first_name', 'username', 'email'
        )


class IncomeForm(forms.Form):
    CATEGORY_CHOICES = [('Зарплата', 'Зарплата'), ('Подарок', 'Подарок'), ('Другое', 'Другое')]

    sum = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Введите сумму'
    }))
    category = forms.ChoiceField(widget=forms.RadioSelect(attrs={
        'class': 'radio-currency'
    }), choices=CATEGORY_CHOICES)
    comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Напишите комментарий'
    }))
    
    class Meta:
        model = Transaction
        fields = (
            'sum', 'category', 'comment'
        )


class OutlineForm(forms.Form):
    CATEGORY_CHOICES = [('Образование', 'Образование'), ('Здоровье', 'Здоровье'), ('Дом', 'Дом')]

    sum = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Введите сумму'
    }))
    category = forms.ChoiceField(widget=forms.RadioSelect(attrs={}), choices=CATEGORY_CHOICES)
    comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Напишите комментарий'
    }))

    class Meta:
        model = Transaction
        fields = (
            'sum', 'category', 'comment'
        )


class CreateWalletForm(forms.Form):
    CURRENCY_CHOICES = [('BYN', 'BYN'), ('USD', 'USD'), ('EUR', 'EUR')]

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Семейный\Личный счет'
    }))
    currency = forms.ChoiceField(widget=forms.RadioSelect(attrs={
    }), choices=CURRENCY_CHOICES)

    class Meta:
        model = Wallet
        fields = (
            'name', 'currency'
        )


class UpdateWalletForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Семейный\Личный счет'
    }))
    target = forms.BooleanField(widget=forms.CheckboxInput(attrs={

    }), required=False)
    class Meta:
        model = Wallet
        fields = (
            'name', 'target'
        )