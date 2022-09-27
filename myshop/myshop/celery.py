"""
Здесь будет происходить настройка celery
 """
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab



# Задаем переменную окружения, содержащую название файла настроек самого проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myshop.settings')
#app = Celery('myshop')
app = Celery('myshop', namespace='CELERY')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# #     # Calls test('hello') every 10 seconds.
# #     # sender.add_periodic_task(60.0, test.s('hello'), name='add every 10')
# #
# #     # Calls test('world') every 30 seconds
# #     # sender.add_periodic_task(60.0, test.s('world'), expires=10)
# #
# #     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(5.0, test.s('Happy Mondays!'),
#     )
#
# @app.task
# def test(arg):
#     print(arg)




app.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'shop.tasks.check',
        'schedule': 10.0,
    },
}
app.conf.timezone = 'UTC'




app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'shop.tasks.add',
        'schedule': crontab(),
        'args': (16, 16)
    },
}


app.conf.beat_schedule = {
    'send-mail-every-week' : {
        'task': 'shop.tasks.send_product_mail_last_week',
        'schedule': crontab(),


    }
}
