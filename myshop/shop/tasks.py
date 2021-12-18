from celery import Celery
from .models import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives


#app = Celery('tasks', broker='pyamqp://guest@localhost//')
app = Celery('tasks', )


@app.task
def send_product_mail(Product):
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
    # data = {'product': Product}
    # subject = 'Новый това'
    # to = []
    # mail = Subscriber.objects.values('user__email')
    # for i in mail:
    #     to.append(i['user__email'])
    # from_email = 'bigmama93@mail.ru'
    # #html = get_template('shop/mail/product_week.html')
    # #html_render = html.render(data)
    # text_content = 'пришел новый товар'
    # msg = EmailMultiAlternatives(subject, text_content, from_email,to)
    # #msg.attach_alternative(html_render,'html/text')
    # msg.send()