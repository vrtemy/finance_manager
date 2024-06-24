from django.shortcuts import render

from finances.services import get_main_wallet


def budgets(request):

    target_wallet = get_main_wallet(request.user)

    context = {
        'title': 'Копилка',
        'target_wallet': target_wallet,
    }
    return render(request, 'budgets/budgets.html', context)
