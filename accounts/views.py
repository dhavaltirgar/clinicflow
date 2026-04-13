from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# -------------------------------------------------------
# Login View — Function Based View (from your PDF!)
# -------------------------------------------------------
def login_view(request):
    # If already logged in — go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = None  # ← store error locally, not in messages

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # ✅ Success message — shows on dashboard
                messages.success(
                    request,
                    f'Welcome back, {user.get_full_name() or user.username}!'
                )
                return redirect('dashboard')
            else:
                # ❌ Error — stored locally, shows on LOGIN page only
                error_message = 'Invalid username or password. Please try again.'
        except Exception as e:
            error_message = 'Something went wrong. Please try again.'

    return render(request, 'accounts/login.html', {
        'error_message': error_message
    })

# -------------------------------------------------------
# Logout View
# -------------------------------------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# -------------------------------------------------------
# Dashboard View — shows summary stats
# -------------------------------------------------------
@login_required
def dashboard(request):
    from patients.models import Patient
    from doctors.models import Doctor
    from appointments.models import Appointment
    from billing.models import Bill
    from django.db.models import Sum

    # Built-in functions + Django ORM — count all records
    context = {
        'total_patients'     : Patient.objects.count(),
        'total_doctors'      : Doctor.objects.count(),
        'total_appointments' : Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'total_revenue'      : Bill.objects.filter(
                                payment_status='paid'
                               ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'recent_appointments': Appointment.objects.select_related(
                                'patient', 'doctor'
                               ).order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)