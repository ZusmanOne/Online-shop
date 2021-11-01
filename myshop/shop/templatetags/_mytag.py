from django import template
from shop.models import *

register = template.Library()


@register.simple_tag(name='sidebar')
def sidebar_tag():
    return Category.objects.all()