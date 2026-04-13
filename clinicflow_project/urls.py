from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Accounts — login, logout
    path('accounts/', include('accounts.urls')),

    # Dashboard
    path('dashboard/', account_views.dashboard, name='dashboard'),

    # Redirect root to dashboard
    path('', account_views.dashboard, name='home'),

    # Apps URLs — we'll add these one by one
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('billing/', include('billing.urls')),
    path('reports/', include('reports.urls')),
    path('prescriptions/', include('prescriptions.urls')),

    path('api/', include('api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)