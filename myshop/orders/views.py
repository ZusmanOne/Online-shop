from django.shortcuts import render
from .models import *
from .forms import *
from cart.cart import Cart


def order_create(request):
    cart=Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product= item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clean_cart()
            return render(request, 'order/created.html', {'order':order})
    else:
        form = OrderForm()
    return render(request, 'order/create.html', {'form':form,'cart': cart})
# Create your views here.
