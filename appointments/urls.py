from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_add, name='appointment_add'),
    path('<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
]