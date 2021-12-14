from django.shortcuts import render,get_object_or_404, HttpResponseRedirect
from .models import *
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def index(request):
    context = Product.objects.all()[:4]
    return render(request, 'shop/index.html', {'context': context})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products,'categories': categories})


def product_detail(request, slug, product_id):
    product_object = get_object_or_404(Product, slug=slug, pk=product_id)
    return render(request, {'product_obj': product_object, 'form': cart_product_form})
# Create your views here.


#товары по категориям
def category_product(request, slug):
    context = Product.objects.filter(category__slug=slug)
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
