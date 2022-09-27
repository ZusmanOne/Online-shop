from django import forms
from .models import *


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'available', 'description']
