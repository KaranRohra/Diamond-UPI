from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_control

from common.models import Requests


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def notification(request):
    if 'email' not in request.COOKIES:
        return redirect('login')
    

    email=request.COOKIES['email']

    recived_request = list(Requests.objects.filter(request_receiver=email))
    sended_request = list(Requests.objects.filter(request_sender=email))


    sorted_data = sorted_on_date_time(recived_request+sended_request)
   
    if sorted_data:
        return render(request, 'notification/notification.html',{
            'noti_data':sorted_data,
            'email':email,
        })
    else:
        return render(request, 'notification/notification.html',{
            'status':'No Notification Available',
        })


def sorted_on_date_time(given: list):
    if len(given)==0:
        return []
    given.sort(key=lambda ele: ele.date, reverse=True)

    result = []

    start_date = given[0].date
    temp = []
    for i in range(len(given)):
        if start_date == given[i].date:
            temp.append(given[i])
        else:
            result.extend(sorted(temp,key = lambda ele: ele.time, reverse=True))
            temp = [given[i]]
            start_date = given[i].date
    result.extend(sorted(temp,key = lambda ele: ele.time, reverse=True))
    return result