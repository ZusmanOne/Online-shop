from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from cart.cart import Cart
from .tasks import order_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from coupons.models import Coupon



def order_create(request):
    cart=Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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

# ФОРМИРОВАНИЕ PDF отчета
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


# Формирование pdf файла о заказе
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content_Disposition'] = 'filename=order_{}'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/shop/css/pdf.css')])
    return response

def home(request):
    return render(request, 'shop/a.html')