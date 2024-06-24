from django.urls import path

from investing.views import dashboard


app_name = 'investing'

urlpatterns = [
    path('', dashboard, name='dashboard')
]

