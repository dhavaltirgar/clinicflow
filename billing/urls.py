from django.urls import path
from . import views

urlpatterns = [
    path('', views.bill_list, name='bill_list'),
    path('add/', views.bill_add, name='bill_add'),
]