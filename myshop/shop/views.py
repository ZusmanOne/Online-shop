from django.shortcuts import render,get_object_or_404
from .models import *


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': categories,
                                                'products': products,
                                                'categories': categories,})


def product_detail(request, slug, product_id):
    product_object = get_object_or_404(Product, slug=slug, pk=product_id)
    return render(request, {'product_obj': product_object})
# Create your views here.
