from django.test import TestCase
from django.urls import reverse
from shop.models import *


class TestIndex(TestCase): # Тест для проверки ответа сервера
    def setUp(self):

        self.product1 = Product.objects.create(category=Category.objects.create(name='snowboarding', slug='snowboard'),
                               name='Burton', price=100.00, description='Good board')
        self.category1 = Category.objects.create(name='snowboarding', slug='snowboard1')
        self.detail_url = reverse('category_product',kwargs={'category_id':self.category1.pk})

    def test_url(self):
        response = self.client.get(self.detail_url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_index_url(self):
        response = self.client.get(reverse('index'),follow=True)
        self.assertEquals(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.client.get(reverse('product_detail', kwargs = {'product_id':self.product1.pk}),  follow=True)
        self.assertEquals(response.status_code,200)

    def