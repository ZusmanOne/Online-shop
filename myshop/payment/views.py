import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO



def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if request.method == "POST":
        # Получение токена для транзакции
        nonce = request.POST.get('payment_method_nonce', None)  # получаем атрибут payment_method_nonce
        # с помощью него сформируем идентификатор платежной транзакции
        # Создание транзакции обращаясь к методу braintree.Transaction.sale, который будет принимать следю аргументы:
        result = braintree.Transaction.sale({
            'amount': f'{total_cost:.2f}',
            # 'amount': '{:.2f}'.format(total_cost),  # общая сумма зааказа
            'payment_method_nonce': nonce,  # токен транзакции
            'options': {
                'submit_for_settlement': True  # (дополнительные параметры. Мы передали значение submit_
                # for_settlement, равное True, благодаря чему транзакция будет обрабатываться автоматически)
            }
        })
        if result.is_success:
            # Отметка заказа как оплаченного
            order.paid = True
            # Сохранение ID транзакции в заказе
            order.braintree_id = result.transaction.id
            order.save()
            # отправление pdf-файла после оплаты
            # создаем эл.сообщение
            subject = 'My shop №{}'.format(order.id)
            message = 'Пожалуйста, найдите в приложении счет за вашу недавнюю покупку.'
            email = EmailMessage(subject,message,'bigmama93@mail.ru', [order.email])
            # формирование самого pdf
            html = render_to_string('order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/shop/css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            # прикрепляем pdf к электронному сообщению
            email.attach('order_{}.pdf'.format(order.id),
                         out.getvalue(),
                         'application/pdf')
            # отправка сообщения
            email.send()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формиование одноразового токена для JavaScript SDK
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def done(request):
    return render(request, 'payment/done.html')


def canceled(request):
    return render(request, 'payment/canceled.html')





# Create your views here.
