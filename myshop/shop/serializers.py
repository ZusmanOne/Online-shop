from django.contrib.auth.models import User, Group
from .models import Product, Category
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = Group
        fields = ['url', 'name']


class CategorySerializer(serializers.ModelSerializer):  # сериализатор для категории
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # здесь указан атрибут сериализатора для категории
    # (FK для модели Product), что бы при  запросе продукта указывался не айди а более подробная информация о категории

    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'created']
