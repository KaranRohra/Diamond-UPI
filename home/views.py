from django.shortcuts import render, redirect
from common.models import Customer
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'email' not in request.COOKIES:
        return redirect('login')

    customer = Customer.objects.get(email_id=request.COOKIES['email'])
    balance = customer.balance
    name = customer.name
    last_login = customer.last_login

    return render(request, 'home/home.html', {
        'name': name,
        'balance': balance,
        'last_login': last_login,
    })
