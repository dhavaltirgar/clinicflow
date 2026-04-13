import functools
from django.shortcuts import redirect
from django.contrib import messages


# -------------------------------------------------------
# How a decorator works:
# @doctor_required above a view function means:
# "Before running this view, check if user is a doctor.
#  If yes → run the view. If no → redirect with error."
# -------------------------------------------------------

def doctor_required(view_func):
    # functools.wraps preserves the original function name
    # This is from your PDF — Decorators topic!
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is logged in AND is a doctor
        if request.user.is_authenticated and request.user.role == 'doctor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request,
                'Access denied! Only doctors can access this page.'
            )
            return redirect('dashboard')
    return wrapper


def admin_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request,
                'Access denied! Only admins can access this page.'
            )
            return redirect('dashboard')
    return wrapper


def admin_or_receptionist_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'receptionist']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request,
                'Access denied! You do not have permission.'
            )
            return redirect('dashboard')
    return wrapper