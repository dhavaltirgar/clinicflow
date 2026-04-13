from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports'),
    path('export/patients/', views.export_patients_csv, name='export_patients'),
    path('export/revenue/', views.export_revenue_csv, name='export_revenue'),
]