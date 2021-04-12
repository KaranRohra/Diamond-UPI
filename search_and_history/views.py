from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection
from django.urls import reverse
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    if 'email' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))

    result = dict(request.GET)

    try:
        email = result['email'][0]
        my_cursor = connection.cursor()

        my_cursor.execute(f"SELECT * FROM COMMON_CUSTOMER WHERE EMAIL_ID LIKE '{email}%' ")

        result = tuple(my_cursor)

        return render(request, 'search_and_history/search.html', {
            'cursor': result,
            'status': True,
            'email': request.COOKIES['email'],
        })
    except:
        render(request, 'search_and_history/search.html')

    return render(request, 'search_and_history/search.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def transaction_history(request):
    try:
        email = request.COOKIES['email']

        my_cursor = connection.cursor()

        my_cursor.execute(f"SELECT * FROM COMMON_TRANSACTIONHISTORY WHERE EMAIL_ID = '{email}' ")

        history = sort_on_date_time(list(my_cursor))

        if history:
            return render(request, 'search_and_history/history.html', {'history': history})
        else:
            return render(request, 'search_and_history/history.html', {'status': 'No History Available'})
    except:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'search_and_history/history.html')


def sort_on_date_time(given: list):
    if  len(given)==0:
        return []
   
    given.sort(reverse=True,key=lambda data:data[4])
    [print(g) for g in given]

    result = []
    start, temp = given[0][4], []
    for i in range(len(given)):
        if start==given[i][4]:
            temp.append(given[i])
        else:
            temp.sort(key=lambda data:data[5])
            result.extend(temp)
            temp = [given[i]]
            start = given[i][4]
    result.extend(temp)
    return result