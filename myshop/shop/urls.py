from django.urls import path,include
from .views import *
from rest_framework import routers


#маршруты для контроллера API сзоданного через класс ViewSets
# router = routers.DefaultRouter() # создали объект DefaultRouter
# router.register('products', ProductViewsSet) # зарегали набор обработчиков с префиксом products


urlpatterns = [
    path('', index, name='index'),
    path('list/<str:slug>', product_list, name='product_list'),
    # path('<int:product_id>/<str:slug>/', product_detail, name='product_detail'),
    path('<int:category_id>/', category_product, name='category_product'),
    path('<int:product_id>', product_detail, name='product_detail'),
    path('accounts/registration/', register_user, name='registration'),
    path('subscriber/',subscriber_user, name='subscriber'),
    path('update_product/<int:product_id>', UpdateProduct, name='update_product'),
    path('api/product/', ProductList.as_view(), name='api_product'),
    # path('api/product/<pk>/', ProductDetailView.as_view(), name='product_detail_api'),
    # path('api/', include(router.urls)),


    # path('', include('social_django.urls')),

]