from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import cache_control

from common.models import *
from datetime import datetime as dt

import pytz
import datetime


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pay(request):
    try:
        request.COOKIES['email']
    except:
        return HttpResponseRedirect(reverse('login'))

    if request.POST:
        data = dict(request.POST)

        amount = int(data['amount'][0])
        password = data['password'][0]

        balance = int(request.COOKIES['balance'])
        if password == request.COOKIES['password'] and amount <= balance and amount>0:
            response = render(request, 'pay_and_request/pay.html', {'status': 'Payment Sussccefull'})

            customer = Customer.objects.get(email_id=request.COOKIES['pay_id'])
            customer = Customer(
                email_id=request.COOKIES['pay_id'],
                balance=customer.balance + amount,
                password=customer.password,
                name=customer.name,
            )
            customer.save()

            customer = Customer(
                email_id=request.COOKIES['email'],
                balance=balance - amount,
                password=request.COOKIES['password'],
                name=request.COOKIES['name'],
            )
            customer.save()

            save_payment_detail(request, 'debited', amount, request.COOKIES['email'], request.COOKIES['pay_id'])
            save_payment_detail(request, 'credited', amount, request.COOKIES['pay_id'], request.COOKIES['email'])

            response.set_cookie('balance', balance - amount)

            response.delete_cookie('pay_id')

            return response
        else:
            return render(request, 'pay_and_request/pay.html', {
                'error_message': 'Insufficient balance or Wrong details',
                'email': request.COOKIES['pay_id'],
            })
    else:
        data = dict(request.GET)
        pay_id = data['email'][0]

        response = render(request, 'pay_and_request/pay.html', {'email': pay_id})
        response.set_cookie('pay_id', pay_id)

        return response


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def requested(request):
    if 'email' not in request.COOKIES:
        return redirect('login')

    if request.POST:
        amount = int(request.POST['amount'])

        if amount<=0:
            return render(request, 'pay_and_request/request.html', {
                'error_message': 'Amount should be greater than 0',
            })

        email = request.COOKIES['email']
        reciver = request.COOKIES['reciver']

        save_request(reciver, email, amount)

        response = render(request, 'pay_and_request/request.html', {
            'status': 'Requested Successfully',
        })

        response.delete_cookie('reciver')

        return response
    else:
        reciver = request.GET['email']

        response = render(request, 'pay_and_request/request.html', {
            'email': reciver,
        })

        response.set_cookie('reciver', reciver)

        return response


def save_request(reciver, sender, amount):
    curr_time_date = str(dt.now(pytz.timezone('Asia/Kolkata'))).split()

    date = curr_time_date[0]
    time = curr_time_date[1].split(".")[0]

    year, month, day = [int(d) for d in date.split("-")]
    hours, minutes, seconds = [int(t) for t in time.split(":")]

    Requests(
        request_receiver=reciver,
        request_sender=sender,
        requested_amount=amount,
        date=datetime.date(year, month, day),
        time=datetime.time(hours, minutes, seconds),
        status='pending',
    ).save()


def save_payment_detail(request, option, amount, email, pay_id):
    curr_time_date = str(dt.now(pytz.timezone('Asia/Kolkata'))).split()

    date = curr_time_date[0]
    time = curr_time_date[1].split(".")[0]

    year, month, day = [int(d) for d in date.split("-")]
    hours, minutes, seconds = [int(t) for t in time.split(":")]

    history = TransactionHistory(
        email_id=email,
        transaction_with=pay_id,
        amount=amount,
        status=option,
        date=datetime.date(year, month, day),
        time=datetime.time(hours, minutes, seconds),
    )
    history.save()
