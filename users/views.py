from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import *
from users.services import create_wallet


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('finances:profile'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('finances:profile'))
        else:
            form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = request.POST['username']
            form.save()
            create_done = create_wallet(user)
            if create_done:
                messages.success(request, 'Регистрация прошла успешно! Войдите.')
            else:
                messages.warning(request, 'Не удалось создать базовый счет!')
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.warning(request, 'Слабый пароль!')
            return HttpResponseRedirect(reverse('users:registration'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)
