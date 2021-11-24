from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.utils import timezone


# контроллер для применения купона
def coupon_apply(request):
    now = timezone.now()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try: # получаем и сверям введенный  купон
                coupon = get_object_or_404(Coupon, code__iexact=code,
                                           valid_from__lte=now,  # дата должна бытьраньше(меньше) или равна сегодняшней
                                           valid_to__gte=now,  # или больше или равна сегодняшней дате
                                           active=True)
                # сохраняем в ссесию введеный купон, присваивая значение по ключу coupon_id
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
    else:
        form = CouponForm()
    return redirect('cart:cart_detail')





# Create your views here.
