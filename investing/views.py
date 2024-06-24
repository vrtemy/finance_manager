from django.shortcuts import render

from finances.services import get_main_wallet
from investing.services import (
    get_coins_data,
    upload_coins_to_db
)


def dashboard(request):
    """ Дашборд с курсом коинов и базовой инфой по каждому коину """
    
    target_wallet = get_main_wallet(request.user)
    coins_data = get_coins_data()

    context = {
        'title': 'Инвестирование',
        'target_wallet': target_wallet,
        'coins': coins_data
    }
    return render(request, 'investing/dashboard.html', context)
