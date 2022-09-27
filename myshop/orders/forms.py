from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        labels = {'first_name': '',
                  'last_name':'',
                  'email':'',
                  'city':'',
                  'postal_code':'',
                  'paid':'',
                  'address':'',
                  }
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'input','placeholder':'Введите Имя'}),
            'last_name':forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите Фамилию'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Введите электронную почту'}),
            'city': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите город'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите адрес'}),
            'postal_code': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите почтовый индекс'}),

                    }