from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from common.models import Customer


def register(request):
	if request.POST:
		data = dict(request.POST)

		try:
			Customer.objects.get(email_id=data['email'][0])

			return render(request, 'register/register.html', {'error_message': 'Account already present'})
		except:
			customer = Customer(
				email_id=data['email'][0],
				password=data['password'][0],
				name=data['name'][0],
				balance=1000
			)
			customer.save()
			return HttpResponseRedirect(reverse('login'))
	else:
		return render(request, 'register/register.html')