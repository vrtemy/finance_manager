from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('', login, name='login'),
    path('registration/', registration, name='registration')
]
