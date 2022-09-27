from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.utils import timezone
from django.views.decorators.http import require_POST


# контроллер для применения купона

def coupon_apply(request):
    now = timezone.now()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:  # получаем и сверям введенный  купон
                coupon = Coupon.objects.get( code__iexact=code,
                                           valid_from__lte=now,  # дата должна бытьраньше(меньше) или равна сегодняшней
                                           valid_to__gte=now,  # или больше или равна сегодняшней дате
                                           active=True)
                # сохраняем в ссесию введеный купон, присваивая значение по ключу coupon_id
                request.session['coupon_id'] = coupon.id
                print('КУПОН')
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
    else:
        request.session['coupon_id'] = None
    return redirect('cart:cart_detail')





