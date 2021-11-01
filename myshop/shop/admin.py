from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ('id', 'name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'available',  'price', 'updated',)
    list_display_links = ('id', 'name', 'created',)
    list_filter = ('available', 'created', 'updated')
    list_editable = ('available', 'price')
    save_on_top = True
    save_as = True


# Register your models here.
