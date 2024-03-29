from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .forms import *
from .cart import Cart
from django.views.decorators.http import require_POST
from coupons.forms import *
from shop.recommender import Recommender


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    coupon_apply_form = CouponForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended = r.suggest_products_for(cart_products, max_results=4)
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form,
                                                'recommended': recommended})


# Create your views here.
