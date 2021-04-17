from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
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
    if 'email' not in request.COOKIES:
        HttpResponseRedirect(reverse('login'))

    email = request.COOKIES['email']

    if 'op' not in request.GET:
        history, count = sort_on_option(request, email)
    else:
        history, count = sort_on_option(request, email, int(request.GET['op']))

    if history:
        response = render(request, 'search_and_history/history.html', {'history': history})
    else:
        response = render(request, 'search_and_history/history.html', {'status': 'No History Available'})

    if 'op' not in request.GET or count is None or count not in range(0, 6):
        response.set_cookie('count', '[0,0,0,0,0,0]')
    else:
        response.set_cookie('count', str(count))

    return response


def sort_on_option(request, email, op=0):
    my_cursor = connection.cursor()

    count = None
    print(request.COOKIES)
    if op != 0:
        count = [int(c) for c in str(request.COOKIES['count'])[1:-1].split(",")]

    query = "SELECT * FROM COMMON_TRANSACTIONHISTORY WHERE EMAIL_ID = '{0}' ORDER BY {1}"
    if op == 0:
        my_cursor.execute(query.format(email, 'DATE DESC, TIME DESC'))
    elif op == 1:
        my_cursor.execute(query.format(email, f'TRANSACTION_WITH {"DESC" if count[1] else "ASC"}'))
    elif op == 2:
        my_cursor.execute(query.format(email, f'STATUS {"DESC" if count[2] else "ASC"}'))
    elif op == 3:
        my_cursor.execute(query.format(email, f'AMOUNT {"DESC" if count[3] else "ASC"}'))
    elif op == 4:
        my_cursor.execute(query.format(email, f'DATE {"DESC" if count[4] else "ASC"}, TIME DESC'))
    elif op == 5:
        my_cursor.execute(query.format(email, f'DATE {"ASC" if count[4] else "DESC"}, TIME {"DESC" if count[5] else "ASC"}'))

    if op != 0:
        count[op] = 0 if count[op] else 1
    return list(my_cursor), count
