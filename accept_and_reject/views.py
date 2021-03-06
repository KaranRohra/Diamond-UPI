from datetime import datetime as dt
import pytz
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from common.models import *


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accept(request):
    if 'email' not in request.COOKIES:
        return redirect('login')

    if request.POST:
        receiver = Requests.objects.get(id=int(request.COOKIES['id']))

        amount = receiver.requested_amount
        password = request.POST['password']
        balance = int(request.COOKIES['balance'])

        if password == request.COOKIES['password'] and balance >= amount > 0:

            save_payment_detail('debited', amount, receiver.request_receiver, receiver.request_sender)
            save_payment_detail('credited', amount, receiver.request_sender, receiver.request_receiver)

            update_balance(receiver.request_receiver, receiver.request_sender, amount)

            Requests.objects.get(id=receiver.id).delete()
            response = render(request, 'accept_and_reject/accept.html', {
                'email': receiver.request_sender,
                'status': 'Payment Successfully Completed',
            })

            response.set_cookie('balance', balance - amount, max_age=1800)
            response.delete_cookie('id')
            return response
        else:
            response = render(request, 'accept_and_reject/accept.html', {
                'email': receiver.request_sender,
                'error_message': 'Insufficient balance or Wrong details'
            })
            return response

    else:
        receiver = Requests.objects.get(id=request.GET['id'])
        response = render(request, 'accept_and_reject/accept.html', {'email': receiver.request_sender})

        response.set_cookie('id', request.GET['id'], max_age=1800)
        return response


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject(request):
    if 'email' not in request.COOKIES:
        return redirect('login')
    if 'id' not in request.GET:
        redirect('search')
    
    id_ = int(request.GET['id'])
    rejected_request = Requests.objects.get(id=id_)

    rejected_request.status = 'rejected'

    rejected_request.save()

    return redirect('notification')


def save_payment_detail(option, amount, email, pay_id):
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


def update_balance(sender, receiver, amount):
    data_of_receiver = Customer.objects.get(email_id=receiver)
    data_of_sender = Customer.objects.get(email_id=sender)

    data_of_receiver.balance += amount
    data_of_sender.balance -= amount

    data_of_receiver.save()
    data_of_sender.save()
