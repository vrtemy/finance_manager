from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages, auth

from finances.forms import *
from finances.services import *
from users.services import create_wallet


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения применены!')
            return HttpResponseRedirect(reverse('finances:profile'))
        else:
            messages.warning(request, 'Что-то пошло не так!')
            return HttpResponseRedirect(reverse('finances:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    user_data = request.user
    yesterday = request.session.get('yesterday')
    wallets = get_wallets(user_data)
    target_wallet = get_main_wallet(user_data)
    transactions = get_transactions_per_day(target_wallet)

    if yesterday is True:
        transactions = get_transactions_per_yesterday(target_wallet)

    # request.session['wallets'] = wallets
    # request.session['target_wallet'] = target_wallet

    context = {
        'title': 'Профиль',
        'form': form,
        'user': user_data,
        'wallets': wallets,
        'target_wallet': target_wallet,
        'transactions': transactions,
        'yesterday': yesterday
    }
    return render(request, 'finances/profile.html', context)


def create_more_wallet(request):
    """ Создание дополнительных счетов пользователя """
    
    target_wallet = get_main_wallet(request.user)

    if request.method == 'POST':
        form = CreateWalletForm(data=request.POST)
        if form.is_valid():
            user = request.user
            name = request.POST['name']
            currency = request.POST['currency']
            new_wallet_created = create_wallet(user, name, currency, False)
            if new_wallet_created:
                messages.success(request, 'Новый счет создан!')
                return HttpResponseRedirect(reverse('finances:profile'))
            else:
                messages.error(request, 'Не удалось создать счет')
                return HttpResponseRedirect(reverse('finances:profile'))
        else:
            messages.warning(request, 'Что-то пошло не так! Попробуйте снова.')
            return HttpResponseRedirect(reverse('finances:create_more_wallet'))
    else:
        form = CreateWalletForm()

    context = {
        'title': 'Создайте счет',
        'form': form,
        'target_wallet': target_wallet

    }
    return render(request, 'finances/create_wallet.html', context)

def update_wallet_data(request):
    """ Обновление существующего счета """
    wallet_data = get_any_wallet(request.session['wallet_id'])
    target_wallet = get_main_wallet(request.user)

    if request.method == 'POST':
        response = update_wallet(
            user=request.user,
            new_name=request.POST['name'],
            wallet_id=request.session['wallet_id'],
            target=True if 'target' in request.POST else False
        )
        if response:
            messages.success(request, 'Данные обновлены!')
            return HttpResponseRedirect(reverse('finances:profile'))
        else:
            messages.warning(request, 'Что-то пошло не так!')
            return HttpResponseRedirect(reverse('finances:update_wallet'))

    initial_data = {
        'name': wallet_data.name,
        'target': wallet_data.target
    }

    form = UpdateWalletForm(initial=initial_data)

    context = {
        'title': 'Измените данные',
        'form': form,
        'wallet': wallet_data,
        'target_wallet': target_wallet,
    }
    return render(request, 'finances/update_wallet.html', context)

def try_delete_wallet(request):
    wallet_id = request.session['wallet_id']
    user = request.user

    deleted = delete_wallet(user=user, wallet_id=wallet_id)

    if deleted:
        messages.success(request, 'Счет удален!')
        return HttpResponseRedirect(reverse('finances:profile'))
    else:
        messages.warning(request, 'Нельзя удалить единственный счет!')
        return HttpResponseRedirect(reverse('finances:update_wallet'))


def wallet_data(request):
    wallet_id = request.POST['wallet_id']

    request.session['wallet_id'] = wallet_id
    request.session.modified = True
    return redirect('finances:update_wallet')


def transactions_per_day(request):
    request.session['yesterday'] = False
    return redirect('finances:profile')

def transactions_per_yesterday(request):
    request.session['yesterday'] = True
    return redirect('finances:profile')


def income(request):
    type_transaction = True  # type(+)
    target_wallet = get_main_wallet(request.user)

    if request.method == 'POST':
        form = IncomeForm(data=request.POST)
        if form.is_valid():
            form_data = request.POST
            user_data = request.user
            try:
                transaction_save(form_data, user_data, type_transaction, target_wallet)
            except ValueError as ex:
                messages.warning(request, ex)
                return HttpResponseRedirect(reverse('finances:profile'))
            except:
                messages.warning(request, 'Не удалось сохранить операцию в базу :(')
                return HttpResponseRedirect(reverse('finances:profile'))
            else:
                balance_change(form_data, type_transaction, target_wallet)
                messages.success(request, 'Операция добавлена! Добавить еще?')
                return HttpResponseRedirect(reverse('finances:profile'))
        else:
            messages.warning(request, 'Что-то пошло не так!')
            return HttpResponseRedirect(reverse('finances:profile'))
    else:
        form = IncomeForm()

    context = {
        'title': 'Операция',
        'type_transaction': type_transaction,
        'target_wallet': target_wallet,
        'form': form
    }
    return render(request, 'finances/type-transaction.html', context)


def outline(request):
    type_transaction = False  # type (-)
    target_wallet = get_main_wallet(request.user)

    if request.method == 'POST':
        form = OutlineForm(data=request.POST)
        if form.is_valid():
            form_data = request.POST
            user_data = request.user
            try:
                transaction_save(form_data, user_data, type_transaction, target_wallet)
            except ValueError as ex:
                messages.warning(request, ex)
                return HttpResponseRedirect(reverse('finances:profile'))
            except:
                messages.warning(request, 'Не удалось сохранить операцию в базу :(')
                return HttpResponseRedirect(reverse('finances:profile'))
            else:
                balance_change(form_data, type_transaction, target_wallet)
                messages.success(request, 'Операция добавлена! Добавить еще?')
                return HttpResponseRedirect(reverse('finances:profile'))
        else:
            messages.warning(request, 'Что-то пошло не так!')
            return HttpResponseRedirect(reverse('finances:profile'))
    else:
        form = OutlineForm()

    context = {
        'title': 'Операция',
        'type_transaction': type_transaction,
        'target_wallet': target_wallet,
        'form': form
    }
    return render(request, 'finances/type-transaction.html', context)


def report(request):
    report_per = request.session.get('report_per')
    user_data = request.user
    target_wallet = get_main_wallet(request.user)

    transactions = get_transaction_for_report(report_per, user_data)
    context = {
        'title': 'Отчет',
        'report_per': report_per,
        'transactions': transactions,
        'user_data': user_data,
        'target_wallet': target_wallet,
    }
    return render(request, 'finances/report.html', context)

def report_per_day(request):
    request.session['report_per'] = 'day'
    return redirect('finances:report')
def report_per_week(request):
    request.session['report_per'] = 'week'
    return redirect('finances:report')
def report_per_month(request):
    request.session['report_per'] = 'month'
    return redirect('finances:report')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))
