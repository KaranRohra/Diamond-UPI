from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from common.models import Customer
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    name = None
    balance = None
    try:
        name = request.COOKIES['name']
        balance = Customer.objects.get(email_id=request.COOKIES['email']).balance

    except:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'home/home.html',{
        'name':name,
        'balance':balance,
        })