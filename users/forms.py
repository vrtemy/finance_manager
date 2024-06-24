from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Логин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'example@gmail.com'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Логин'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль'
    }))
    
    class Meta:
        model = User
        fields = (
            'first_name', 'email', 'username', 'password1', 'password2'
        )