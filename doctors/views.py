from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor

@login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'doctors/list.html', {'doctors': doctors})

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/detail.html', {'doctor': doctor})