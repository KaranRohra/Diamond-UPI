from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse

from common.public import *
from common.models import Customer


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_profile(request):
    if 'email' not in request.COOKIES:
        return redirect('logout')
    email = request.COOKIES['email']
    customer_curr_data = {
        'email': email,
        'name': request.COOKIES['name'],
        'password': request.COOKIES['password'],
    }
    if request.POST:
        otp = request.POST['otp']
        if 'otp' in request.COOKIES and otp == request.COOKIES['otp']:
            update_customer_data(email, request.POST['name'], request.POST['password'])
            return render(request, 'profile/profile.html', {'status': 'Profile updated Successfully'})
        else:
            return render(request, 'profile/profile.html', {'error_message': 'Wrong OTP or OTP expired'})
    elif 'otp_status' in request.GET:
        if 'otp' not in request.COOKIES:
            otp = generate_otp()

            print(otp)
            
            is_otp_send = send_mail(email, otp)

            response = HttpResponseRedirect(reverse('profile'))
            response.set_cookie("error_message", "OTP Send Successfully" if is_otp_send else "Failed while Sending OTP", max_age=120)
            if is_otp_send:
                response.set_cookie('otp', otp, max_age=120)
            return response
        else:
            response = HttpResponseRedirect(reverse('profile'))
            response.set_cookie("error_message", "OTP Already Send Successfully", max_age=120)
            return response

    response = render(request, 'profile/profile.html', customer_curr_data)
    if "error_message" in request.COOKIES:
        print(request.COOKIES['error_message'])
        customer_curr_data["error_message"] = request.COOKIES["error_message"]
        response = render(request, 'profile/profile.html', customer_curr_data)
        response.delete_cookie("error_message")
       
    return response


def update_customer_data(email, name, password):
    customer = Customer.objects.get(email_id=email)
    customer.name = name
    customer.password = password
    customer.save()
