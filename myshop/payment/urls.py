from django.urls import path
from .views import *


app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='process'),
    path('done/',   done, name='done'),
    path('canceled/', canceled, name='canceled'),
]