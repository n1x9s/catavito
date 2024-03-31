from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cat
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    cats = Cat.objects.all()
    return render(request, 'catshop/index.html', {'cats': cats})


def show_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    return render(request, 'catshop/show.html', {'cat': cat})


def about(request):
    return render(request, 'catshop/about.html')


def buy_cat(request, cat_id):
    if request.method == 'POST':
        cat = Cat.objects.get(pk=cat_id)
        token = request.POST.get('stripeToken')
        try:

            price = int(float(cat.price))
            charge = stripe.Charge.create(
                amount=price,
                currency='rub',
                description=f'Оплата за котика {cat.name}',
                source=token,
            )
            messages.success(request, f'Вы успешно приобрели котика {cat.name} за {cat.price}!')
            return redirect('index')
        except stripe.error.CardError as e:
            messages.error(request, f'Ошибка платежа: {e.error.message}')
            return redirect('index')
    else:
        return redirect('index')