from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from common.models import Customer


def login(request):
    if request.POST:
        data = dict(request.POST)

        email = data['email'][0]
        password = data['password'][0]
        try:
            
            customer = Customer.objects.get(email_id=email)
        
            if customer.password == password:
                response = HttpResponseRedirect(reverse('home'))

                response.set_cookie('email', customer.email_id)
                response.set_cookie('password', customer.password)
                response.set_cookie('name',customer.name)
                response.set_cookie('balance', customer.balance)

                return response 
            else:
                return render(request, 'login/login.html', {'error_message':'Wrong password'})
        except:
            return render(request,  'login/login.html', {'error_message':'Account does not exists'})
    else:
        return render(request, 'login/login.html')


def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    [response.delete_cookie(key) for key in request.COOKIES]

    return response