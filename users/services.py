from users.models import User
from finances.models import Wallet


def create_wallet(user, name='Основной счет', currency='USD', target='True'):
    """ Создание базового кошелька при создании пользователя """

    if type(user) == type('str'):
        model = Wallet(
            user = User.objects.get(username=user),
            name = name,
            currency = currency,
            target = target
        )
    else:
        model = Wallet(
            user = User.objects.get(username=user.username),
            name = name,
            currency = currency,
            target = target
        )
    try:
        model.save()
    except:
        return False
    else:
        return True
    