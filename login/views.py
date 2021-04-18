import pytz
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from common.models import Customer
from django.core.exceptions import  ObjectDoesNotExist
from datetime import datetime
import datetime as datetime_


def login(request):
    if request.POST:
        data = dict(request.POST)

        email = data['email'][0]
        password = data['password'][0]
        try:

            customer = Customer.objects.get(email_id=email)

            if customer.password == password:
                response = HttpResponseRedirect(reverse('home'))

                response.set_cookie('email', customer.email_id, max_age=1800)
                response.set_cookie('password', customer.password, max_age=1800)
                response.set_cookie('name', customer.name, max_age=1800)
                response.set_cookie('balance', customer.balance, max_age=1800)

                customer.last_login = customer.curr_login
                customer.curr_login = get_curr_time()
                customer.save()

                return response
            else:
                return render(request, 'login/login.html', {'error_message': 'Wrong password'})
        except ObjectDoesNotExist:
            return render(request, 'login/login.html', {'error_message': 'Account does not exists'})
    else:
        return render(request, 'login/login.html')


def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    [response.delete_cookie(key) for key in request.COOKIES]

    return response


def get_curr_time():
    curr = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()
    date = curr[0]
    time = curr[1].split(".")[0]
    year, month, day = [int(d) for d in date.split("-")]
    hours, minutes, seconds = [int(t) for t in time.split(":")]
    return datetime.combine(datetime_.date(year, month, day), datetime_.time(hours, minutes, seconds))
