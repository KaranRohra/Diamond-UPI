from . import views
from django.urls import path

urlpatterns = [
    path('',views.login, name="login"),
    path('logout', views.logout, name="logout")
]
