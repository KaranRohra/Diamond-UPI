from . import views
from django.urls import path

urlpatterns = [
    path('search_customer/',views.search, name='search'),
    path('transaction_history/',views.transaction_history, name='history'),
]
