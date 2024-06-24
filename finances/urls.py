from django.urls import path

from finances.views import *

app_name = 'finances'

urlpatterns = [
    path('profile/', profile, name='profile'),
    # path('transaction/', transaction, name='transaction'),
    path('create_wallet', create_more_wallet, name='create_wallet'),
    path('update_wallet', update_wallet_data, name='update_wallet'),
    path('delete_wallet', try_delete_wallet, name='delete_wallet'),
    path('wallet_data', wallet_data, name='wallet_data'),
    path('transactions_per_day', transactions_per_day, name='transactions_per_day'),
    path('transactions_per_yesterday', transactions_per_yesterday, name='transactions_per_yesterday'),
    path('income/', income, name='income'),
    path('outline/', outline, name='outline'),
    path('report/', report, name='report'),
    path('report_per_day/', report_per_day, name='report_per_day'),
    path('report_per_week/', report_per_week, name='report_per_week'),
    path('report_per_month/', report_per_month, name='report_per_month'),
    path('logout/', logout, name='logout')
]

