from . import views
from django.urls import path

urlpatterns = [
    path('pay/',views.pay, name='pay'),
    path('request/',views.requested, name='requested'),
]

