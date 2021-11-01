from django.shortcuts import render,get_object_or_404
from .models import *
from cart.forms import CartAddProductForm


def index(request):
    return render(request, 'shop/index.html')


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
    return render(request, 'shop/single_product.html', {'object':object,'form': cart_product_form })

