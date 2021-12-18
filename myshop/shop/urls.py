from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('list/', product_list, name='product_list'),
    path('<int:product_id>/<str:slug>/', product_detail, name='product_detail'),
    path('<int:category_id>/', category_product, name='category_product'),
    path('<int:product_id>', product_detail, name='product_detail'),
    path('accounts/registration/', register_user, name='registration'),
    path('subscriber/',subscriber_user, name='subscriber'),

    # path('', include('social_django.urls')),

]