from celery import Celery
from .models import *
from django.core.mail import send_mail


#app = Celery('tasks', broker='pyamqp://guest@localhost//')
app = Celery('tasks', )


@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Заказ № %s' % order.id
    message = 'Здравствуйте %s,\n\n Ваш заказ успешно сформирован.\
    Номер Заказа %s.' % (order.first_name,order.id)
    mail_sent = send_mail(subject,
                          message,
                          'bigmama93@mail.ru',
                          [order.email])
    return mail_sent

