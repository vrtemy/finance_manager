from django.utils import timezone
from datetime import timedelta
from finances.models import Transaction, TransactionCategory
from users.models import User, Wallet


def get_main_wallet(user_data):
    
    user = User.objects.get(id=user_data.id)
    try:
        wallet_data = Wallet.objects.get(user=user, target=True)
    except:
        wallets = Wallet.objects.filter(user=user)
        test = []
        for wallet in wallets:
            test.append(wallet.id)
        make_target = Wallet.objects.get(id=min(test))
        make_target.target = True
        make_target.save()
        print('MAIN WALLET IS CHANGED!')
        get_main_wallet(user_data)
    else:
        return wallet_data

def get_wallets(user_data):
    user = User.objects.get(id=user_data.id)
    wallets = Wallet.objects.filter(user=user)
    return wallets

def get_any_wallet(wallet_id):
    wallet_data = Wallet.objects.get(id=wallet_id)
    return wallet_data

def update_wallet(user, new_name, wallet_id, target):
    
    wallet = Wallet.objects.get(id=wallet_id)

    if wallet.target != target:
        try:
            before_target_wallet = get_main_wallet(user)
            before_target_wallet.target = False
            before_target_wallet.save()
            wallet.target = target
            wallet.name = new_name
            wallet.save()
        except:
            print('ERROR UPDATE')
            return False
        else:
            print('WALLET SAVED!')
            wallet.save()
            return True
    else:
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            wallet.name = new_name
        except:
            print('ERROR UPDATE')
            return False
        else:
            print('WALLET SAVED!')
            wallet.save()
            return True

def delete_wallet(user, wallet_id):
    user = User.objects.get(id=user.id)
    wallet = Wallet.objects.get(id=wallet_id)

    if len(Wallet.objects.filter(user=user)) > 1:
        try:
            wallet.delete()
            return True
        except:
            return False
    else:
        return False
        


def transaction_save(form_data, user_data, type_transaction, target_wallet):
    """ Сохранение транзакции в базу """
    sum = float(form_data['sum'])
    balance = target_wallet.balance
    
    model = Transaction(
        type=type_transaction,
        user=User.objects.get(id=user_data.id),
        wallet=target_wallet,
        sum=sum,
        category=TransactionCategory.objects.get(name=form_data['category']),
        comment=form_data['comment']
    )
    try:
        if type_transaction is True and 0 < sum:
            if sum < 1_000_000_000:
                model.save()
            else:
                raise ValueError('Слишком большая сумма!')
        elif type_transaction is False and 0 < sum:
            if sum <= balance:
                model.save()
            else:
                raise ValueError('Сумма больше баланса!')
        else:
            raise ValueError('Сумма меньше 0!')
    except:
        raise ValueError('Что-то пошло не так!')


def balance_change(form_data, type_transaction, target_wallet):
    """ Манипуляция с балансом после оформленной операции """
    wallet = target_wallet
    balance = float(wallet.balance)
    type = type_transaction
    sum = float(form_data['sum'])

    if type is True:
        new_balance = balance + sum
    elif type is False:
        new_balance = balance - sum

    wallet.balance = new_balance
    wallet.save()


def get_transactions_per_day(target_wallet):
    # wallet = Wallet.objects.get(id=target_wallet.id)

    today_date = timezone.now().date()
    today_transactions = Transaction.objects.filter(date=today_date, wallet=target_wallet)
    return today_transactions

def get_transactions_per_yesterday(target_wallet):
    # wallet = Wallet.objects.get(id=target_wallet.id)

    yesterday_date = timezone.now().date() - timedelta(days=1)
    yesterday_transactions = Transaction.objects.filter(date=yesterday_date, wallet=target_wallet)
    return yesterday_transactions


def get_transaction_for_report(report_per, user_data):
    user = User.objects.get(id=user_data.id)

    today_date = timezone.now().date()
    one_week_ago = today_date - timedelta(weeks=1)
    one_month_ago = today_date - timedelta(weeks=4)

    if report_per == 'day':
        transactions = Transaction.objects.filter(user=user, date=today_date)
    elif report_per == 'week':
        transactions = Transaction.objects.filter(user=user, date__range=(one_week_ago, today_date))
    elif report_per == 'month':
        transactions = Transaction.objects.filter(user=user, date__range=(one_month_ago, today_date))
    else:
        transactions = Transaction.objects.filter(user=user)

    return transactions
