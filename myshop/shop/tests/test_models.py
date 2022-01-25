from django.test import TestCase

from shop.models import Category, Product

class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name = 'snowboarding', slug='snowboard')

    def test_name_label(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Наименование')

    def test_slug_field(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('slug').max_length
        self.assertEqual(field_label, 100)

    def test_get_absolute_url(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(category.get_absolute_url(), '/list/snowboard')

class TestProductCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        Product.objects.create(category=Category.objects.create(name='snowboarding', slug='snowboard'),
                               name='Burton', price=100.00, description='Good board')

    def test_field_label(self):
        product = Product.objects.get(pk=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название товара')

    def test_get_absolute_url(self):
        product = Product.objects.get(pk=1)
        self.assertEqual(product.get_absolute_url(),'/1')