from django.shortcuts import render, redirect
from .models import *
from .forms import *
from cart.cart import Cart
from .tasks import order_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.urls import reverse


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
            order_created.delay(order.id) # запуск асинхронной задачи celery
            # сохранение заказа сессии
            request.session['order_id']= order.id
            # перенапарление на страницу оплтаты в кач-ве аргумента название контроллера(т.е. имени маршрута его)
            return redirect(reverse('payment:process'))
    else:
        form = OrderForm()
    return render(request, 'order/create.html', {'form':form,'cart': cart})
# Create your views here.

# отправлениe сообщения на почту
# def order_message(order_id):
#     orders = Order.objects.get(id=order_id)
#     print(orders.id)
#     subject = 'номер заказа'
#     message = 'Здрасте  ваш номер заказа успешно оформлен'
#     mail = send_mail(subject,message,from_email='bigmama93@mail.ru', recipient_list=[orders.email])
#     return mail


# @receiver(post_save, sender=Order)
# def create_order(instance, created, **kwargs):
#     if created:
#         order_message(instance.pk)
#         print('почта отправлена')