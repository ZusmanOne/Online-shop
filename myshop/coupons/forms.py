from .models import *
from django import forms
from orders.models import Order

class CouponForm(forms.Form):
    code = forms.CharField(max_length=50, label='',)
    # def clean_code(self):
    #     my_code = self.cleaned_data['code']
    #     code_order = Order.coupon
    #     if my_code
