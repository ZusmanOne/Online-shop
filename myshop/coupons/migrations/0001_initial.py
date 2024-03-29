# Generated by Django 3.2.8 on 2021-11-23 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Промокод')),
                ('valid_from', models.DateTimeField(help_text='Дата начала действия купона', verbose_name='Начало')),
                ('valid_to', models.DateTimeField(help_text='Дата окончания действия купона', verbose_name='Окончание')),
                ('discount', models.IntegerField(help_text='Размер скидки в %', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка')),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
    ]
