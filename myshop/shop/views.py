from django.shortcuts import render,get_object_or_404, HttpResponseRedirect, redirect
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



@login_required(login_url='/accounts/login/')
def index(request):
    context = Product.objects.all()[:4]
    return render(request, 'shop/index.html', {'context': context})


@login_required()
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products,'categories': categories})


@login_required()
def product_detail(request, slug, product_id):
    product_object = get_object_or_404(Product, slug=slug, pk=product_id)
    return render(request, {'product_obj': product_object, 'form': cart_product_form})
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


def send_mail_product(Product):
    subject = 'Новинка недели'
    from_email = 'bigmama93@mail.ru'
    mail = Subscriber.objects.values('user__email')
    to = []
    for i in mail:
        to.append(i['user__email'])
    html_content = get_template('shop/mail/product_week.html')
    context = {'product': Product}
    html_render = html_content.render(context)
    msg = EmailMultiAlternatives(subject=subject,body=html_render,to=to, from_email=from_email)
    msg.attach_alternative(html_render, 'text/html')
    msg.send()


@receiver(post_save, sender=Product)
def send_for_product_week(instance,created, **kwargs):
    if created:
        send_mail_product(instance)
        print('почта отправлена')
