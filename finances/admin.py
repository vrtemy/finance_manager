from django.contrib import admin
from finances.models import *


admin.site.register(TransactionCategory)
admin.site.register(Transaction)
admin.site.register(Wallet)