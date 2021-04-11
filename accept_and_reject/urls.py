from . import views
from django.urls import path

urlpatterns = [
    path('accept/', views.accept, name='accept'),
    path('reject/', views.reject, name='reject'),
]
