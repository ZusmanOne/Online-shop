"""
Здесь будет происходить настройка celery
 """
import os
from celery import Celery
from django.conf import settings



# Задаем переменную окружения, содержащую название файла настроек самого проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myshop.settings')
#app = Celery('myshop')
app = Celery('myshop', namespace='CELERY')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


