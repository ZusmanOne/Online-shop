from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import *
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives # отправка писем с разным содержимым
from django.template.loader import get_template
from django.dispatch import receiver
from django.db.models.signals import post_save
from shop.tasks import send_product_mail
from django.core.cache import cache
from .forms import *



@login_required(login_url='/accounts/login/')
def index(request):
    context = Product.objects.all()[:4]
    num_visit = request.session.get('num_visit',0)
    request.session['num_visit'] = num_visit + 1
    # visit = cache.get_or_set('num_visit', num_visit, 10)
    return render(request, 'shop/index.html', {'context': context, 'num_visits':num_visit,})


@login_required()
def product_list(request, slug):
    categories = Category.objects.filter(slug=slug)
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products,'categories': categories})


# @login_required()
# def product_detail(request, slug, product_id):
#     product_object = get_object_or_404(Product, slug=slug, pk=product_id)
#     return render(request, {'product_obj': product_object, 'form': cart_product_form})
# Create your views here.


#товары по категориям
@login_required()
def category_product(request, category_id):
    context = Product.objects.filter(category_id=category_id)
    return render(request, 'shop/category_product.html', {'context': context})


def product_detail(request, product_id):
    object = get_object_or_404(Product, pk=product_id)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    bought_product = r.products_bought([object])
    print(bought_product)
    recommended_products = r.suggest_products_for([object],4)
    print(recommended_products)
    return render(request, 'shop/single_product.html', {'object':object,'form': cart_product_form,
                                                        'recommended': recommended_products})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request,'registration/registration.html', {'form':form})


def subscriber_user(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            created = Subscriber.objects.get_or_create(user=request.user)
        return redirect('/')


def send_mail_product(product_id):
    data = Product.objects.get(name=product_id)
    subject = 'Новинка недели'
    from_email = 'bigmama93@mail.ru'
    mail = Subscriber.objects.values('user__email')
    to = []
    for i in mail:
        to.append(i['user__email'])
    html_content = get_template('shop/mail/product_week.html')
    context = {'product': data}
    html_render = html_content.render(context)
    msg = EmailMultiAlternatives(subject=subject,body=html_render,to=to, from_email=from_email)
    msg.attach_alternative(html_render, 'text/html')
    msg.send()


@receiver(post_save, sender=Product)
def send_for_product_week(instance,created,**kwargs):
    if created:
        send_product_mail.delay(instance.name)


def UpdateProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, instance=product) # при редактировании передаем объект product в аргумент
        # instance
        if form.is_valid():
            product_update = product.save()
            return redirect(product)
    else:
        form = UpdateProductForm(instance=product)
    return render(request, 'shop/update_product.html', {'form': form})


"""
здесь будет описываться приложение для DRF
"""

from django.contrib.auth.models import User,Group
from rest_framework import viewsets,permissions
from shop.serializers import  ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     Конечная точка API, которая позволяет просматривать или редактировать пользователей.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# # class ProductsViewSet(viewsets.ModelViewSet):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer
# #     permission_classes = [permissions.IsAuthenticated]
#
# @api_view(['GET'])
# def api_product(request):
#     if request.method == 'GET':
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many = True) # many значит что нужно показывать все объекты
#         return Response(serializer.data)
#
#
# #сведения о каждом продукте
# @api_view(['GET'])
# def api_product_detail(request, product_id):
#     if request.method == 'GET':
#         queryset = Product.objects.filter(pk=product_id)
#         serializer =ProductSerializer(queryset)
#         return Response(serializer.data)
#
#
# #свдеения о продуктах через класс
# class ProductListView(generics.ListAPIView):  # только для чтения для представления коллекции экземпляров модели .
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductDetailView(generics.RetrieveAPIView):  # только для чтения для представления одного экземпляра модели .
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductViewsSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


from rest_framework.views import APIView


class ProductList(APIView): # апи для всех сниппетов, реализованный через CBV
    """
    Отображает все сниппеты или создает новый сниппет.
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        snippet = Product.objects.all()
        serializer = ProductSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)