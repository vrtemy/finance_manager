from django.urls import path

from budgets.views import budgets


app_name = 'budgets'

urlpatterns = [
    path('', budgets, name='budgets')
]

