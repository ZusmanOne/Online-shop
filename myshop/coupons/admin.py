from django.contrib import admin
from .models import *


class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount', 'valid_from', 'valid_to', 'active',)
    list_display_links = ('id', 'code', 'discount',)
    list_filter = ('active', 'valid_from', 'valid_to',)
    search_fields = ('code',)


admin.site.register(Coupon, CouponAdmin)
# Register your models here.
