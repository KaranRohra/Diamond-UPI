from django.db import models


class Customer(models.Model):
	email_id = models.EmailField(max_length=50, primary_key=True)
	password = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	balance = models.IntegerField(default=0)


class TransactionHistory(models.Model):
	email_id = models.EmailField(max_length=50)
	transaction_with = models.EmailField(max_length=50, default=None)
	amount = models.IntegerField()
	status = models.CharField(max_length=50, default=None,
		choices=(
				('credited','credited'),
				('debited','debited'),
			)
		)
	date = models.DateField(auto_now=False, auto_now_add=False, default=None)
	time = models.TimeField(auto_now=False, auto_now_add=False, default=None)


class Requests(models.Model):
	request_receiver = models.EmailField(max_length=50)
	request_sender = models.EmailField(max_length=50)
	requested_amount = models.IntegerField()
	date = models.DateField(auto_now=False, auto_now_add=False, default=None)
	time = models.TimeField(auto_now=False, auto_now_add=False, default=None)
	status = models.CharField(max_length=50, default=None,
		choices=(
				('accepted','accepted'),
				('rejected','rejected'),
				('pending','pending'),
			)
		)
