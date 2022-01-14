from django import template
from shop.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='sidebar')
def sidebar_tag():
    return Category.objects.all()


@register.inclusion_tag('shop/visit_tag.html')
def count_visit(request):
    num_visit = request.session.get('num_visit',0)
    request.session['num_visit'] = num_visit + 1
    return {'num_visits': num_visit}
