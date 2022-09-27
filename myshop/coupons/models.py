from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator # для проверки значений поля discount


class Coupon(models.Model):
    code = models.CharField(max_length=50, verbose_name='Промокод')
    valid_from = models.DateTimeField(help_text='Дата начала действия купона', verbose_name='Начало')
    valid_to = models.DateTimeField(help_text='Дата окончания действия купона', verbose_name='Окончание')
    discount = models.IntegerField(help_text='Размер скидки в %', verbose_name='Скидка',
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


# Create your models here.
