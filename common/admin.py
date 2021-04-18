from django.contrib import admin
from .models import *


@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ('email_id', 'password', 'name', 'balance', 'last_login', 'curr_login')


@admin.register(Requests)
class AdminRequests(admin.ModelAdmin):
    list_display = ('request_receiver', 'request_sender', 'requested_amount', 'date', 'time', 'status')


@admin.register(TransactionHistory)
class AdminTransactionHistory(admin.ModelAdmin):
    list_display = ('email_id', 'transaction_with', 'amount', 'date', 'time', 'status')
