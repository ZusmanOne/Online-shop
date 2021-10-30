from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('list/', product_list, name='product_list'),
    path('<int:product_id>/<str:slug>/', product_detail, name='product_detail'),
    path('<str:slug>/', category_product, name='category_product'),
]