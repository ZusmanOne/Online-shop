from django.contrib import admin
from .models import *
import csv
import datetime
from django.http import HttpResponse
from django.shortcuts import reverse
from django.utils.safestring import mark_safe


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


def export_to_csv(modeladmin, request, queryset): # ф-ия котор. экспортирует объеткты Orders в csv-файл
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')  # созд-ие объекта-ответа класса HttpResponse с типо содержимым csv
    response['Content-Disposition'] = content_disposition # добавляем заголовок т.к к ответу будет прикрепелн файл
    writer = csv.writer(response) # создаем объект котор. будет записывать данные файла в обхект response
    # получаем поля модели(через опцию meta модели) исключая те у которых  связи ManyToMany и OneToMany
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Записываем  в файл первую строку с названием полей
    writer.writerow([field.verbose_name for field in fields])
    # Записываем данные
    for obj in queryset: # проходим по объектам выбранным юзером
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'city', 'created', 'paid', order_pdf]
    list_display_links = ('id', 'first_name', 'last_name')
    list_editable = ('paid',)
    list_filter = ('created', 'paid', 'city')
    inlines = [OrderItemInLine]
    actions = [export_to_csv]



admin.site.register(Order, OrderAdmin)

# Register your models here.
