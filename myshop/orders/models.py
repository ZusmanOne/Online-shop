from django.db import models
from shop.models import Product


class Order(models.Model): # модель покупателя
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, help_text="Оплачен ли заказ?")
    braintree_id = models.CharField(max_length=150, blank=True)# это поле нужно ждя лпаты заказа(уникальный ID платежа)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return "Заказ №  %s" % self.pk

    def get_total_cost(self): # метод чтобы получить общую стоимость товаров в заказе
        return sum(item.get_cost() for item in self.product_items.all())


class OrderItem(models.Model): # Модель заказанного товара
    order = models.ForeignKey(Order,related_name='product_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Стоимость корзины')
    quantity = models.PositiveIntegerField(default=1, help_text='Количество товара в корзине')

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'



    def get_cost(self):
        return self.price * self.quantity










# Create your models here.
