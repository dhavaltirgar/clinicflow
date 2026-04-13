from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)
from . import views

urlpatterns = [

    # ---- JWT Authentication ----
    path('auth/login/',
         views.api_login,
         name='api_login'),

    path('auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain'),

    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    # ---- Dashboard ----
    path('dashboard/',
         views.api_dashboard,
         name='api_dashboard'),

    # ---- Patients ----
    path('patients/',
         views.PatientListCreateView.as_view(),
         name='api_patient_list'),

    path('patients/<int:pk>/',
         views.PatientDetailView.as_view(),
         name='api_patient_detail'),

    # ---- Doctors ----
    path('doctors/',
         views.DoctorListView.as_view(),
         name='api_doctor_list'),

    path('doctors/<int:pk>/',
         views.DoctorDetailView.as_view(),
         name='api_doctor_detail'),

    # ---- Appointments ----
    path('appointments/',
         views.AppointmentListCreateView.as_view(),
         name='api_appointment_list'),

    path('appointments/<int:pk>/',
         views.AppointmentDetailView.as_view(),
         name='api_appointment_detail'),

    # ---- Prescriptions ----
    path('prescriptions/',
         views.prescription_api,
         name='api_prescription'),

    # ---- Billing ----
    path('bills/',
         views.BillListCreateView.as_view(),
         name='api_bill_list'),

    path('bills/<int:pk>/',
         views.BillDetailView.as_view(),
         name='api_bill_detail'),
]