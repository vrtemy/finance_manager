from django.urls import path
from pdf_gen.views import *

app_name = 'pdf_gen'

urlpatterns = [
    path('pdf_generation/', pdf_generation, name='pdf_generation')
]