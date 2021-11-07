from django.contrib import admin
from .models import *


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'email','city','created','paid')
    list_display_links = ('id','first_name', 'last_name')
    list_editable = ('paid',)
    list_filter = ('created','paid','city')
    inlines = [OrderItemInLine]

admin.site.register(Order,OrderAdmin)

# Register your models here.
