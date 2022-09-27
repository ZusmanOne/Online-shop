from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create_order/', order_create, name = 'order_create'),
    path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name = 'admin_order_pdf'),
    path('test1/', home, name='home'),
]