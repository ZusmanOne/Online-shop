from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 100, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('product_list', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название товара')
    image = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    description = models.TextField(verbose_name='Описание товара', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.pk})


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return str(self.user)
# Create your models here.
