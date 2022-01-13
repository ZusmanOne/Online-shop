from celery import Celery
from .models import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
# import datetime, pytz

#app = Celery('tasks', broker='pyamqp://guest@localhost//')
app = Celery('tasks', )


@app.task(name='shop.tasks.check')
def check():
    print('I am checking your stuff')


@app.task
def add(x, y):
    z = x + y
    print(z)


@app.task
def send_product_mail(Product):
    #OurTZ = pytz.timezone('Europe/Moscow')
    #last_week = datetime.datetime.now(OurTZ) - datetime.timedelta(days=7)
    product = Product.objects.all[1]
    subject = 'Новинка недели'
    from_email = 'bigmama93@mail.ru'
    mail = Subscriber.objects.values('user__email')
    to = []
    for i in mail:
        to.append(i['user__email'])
    html_content = get_template('shop/mail/product_week.html')
    context = {'product': product}
    html_render = html_content.render(context)
    msg = EmailMultiAlternatives(subject=subject,body=html_render,to=to, from_email=from_email)
    msg.attach_alternative(html_render, 'text/html')
    msg.send()

@app.task
def send_product_mail_last_week():
    #OurTZ = pytz.timezone('Europe/Moscow')
    #last_week = datetime.datetime.now(OurTZ) - datetime.timedelta(days=7)
    product = Product.objects.all()
    product1 = product[1]
    subject = 'Новинка недели'
    from_email = 'bigmama93@mail.ru'
    mail = Subscriber.objects.values('user__email')
    to = []
    for i in mail:
        to.append(i['user__email'])
    html_content = get_template('shop/mail/product_week.html')
    context = {'product': product1}
    html_render = html_content.render(context)
    msg = EmailMultiAlternatives(subject=subject,body=html_render,to=to, from_email=from_email)
    msg.attach_alternative(html_render, 'text/html')
    msg.send()

