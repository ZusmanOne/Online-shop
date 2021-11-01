from decimal import Decimal
from django.conf import settings
from shop.models import *


class Cart(object): # Этот класс будет отвечать за работу с корзинми покупок
    def __init__(self, request): # при инициализации обхекта необходимо передать объект запроса request
        """ Инициализация объекта корзины"""
        self.session = request.session # запоминаем текущую сессию, что бы иметь к ней длступ в другиз метода класса
        # она равна сессии из запроса
        cart = self.session.get[settings.SESSION_CART_ID] # получаем данные из корзины
        if not cart: # если их нет, создаем ее как пустой словарь в сесии
            cart = self.session.[settings.SESSION_CART_ID]={}
        self.cart = cart

    def add(self, product, quantity = 1, update_quantity=False):
        """Добавление товаров в корщину или обновлени его количества"""
        product_id = str(product.id) # преобразуем ИД товара в стрроку для представления в JSON
        if product.id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price':str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True
        """ Метод save() помечает сессию как измененную с помощью атрибута 
            modified – session.modified = True. Так мы говорим Django о том, что редактировали
        данные сессии, а теперь их необходимо сохранить."""

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            """Метод remove() удаляет товар из корзины и сохраняет новые данные сессии,
обращаясь к методу save()"""


    """для отображения товаров помещенных в корзину нужно проходиться циклом по продуктам и проверять их"""
    def __iter__(self):
        product_ids = self.cart.keys() # получаем все ключи продуктов в корзине
        products = Product.objects.filter(id__in = product_ids) # Получаем объекты модели и передаем в корзину
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item


    def __len__(self): # метод для общего количестов товаров в корзине
        for item in self.cart.values():
           return sum(item['quantity'])


    def total_price(self): # метод для общей суммы
        for item in self.cart.values():
            return sum(Decimal(item['price']) * item['quantity'])

    def clean_cart(self): # метод очистки корзины
        del self.session[settings.CART_SESSION_ID]
        self.save()



