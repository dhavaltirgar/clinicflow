from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):
    # Search functionality using built-in filter
    search = request.GET.get('search', '')
    if search:
        # Using OR operator — search in multiple fields
        patients = Patient.objects.filter(
            first_name__icontains=search
        ) | Patient.objects.filter(
            last_name__icontains=search
        ) | Patient.objects.filter(
            phone__icontains=search
        )
    else:
        patients = Patient.objects.all()

    # Built-in len() function
    total = len(list(patients))

    return render(request, 'patients/list.html', {
        'patients' : patients,
        'search'   : search,
        'total'    : total
    })


@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        # Exception Handling — what if form has errors?
        try:
            if form.is_valid():
                patient = form.save()
                messages.success(
                    request,
                    f'Patient {patient} added successfully!'
                )
                return redirect('patient_list')
            else:
                messages.error(request, 'Please fix the errors below.')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
    else:
        form = PatientForm()

    return render(request, 'patients/form.html', {
        'form'  : form,
        'action': 'Add Patient'
    })


@login_required
def patient_edit(request, pk):
    # get_object_or_404 — Exception Handling!
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        # instance=patient tells Django to UPDATE, not create new
        form = PatientForm(request.POST, instance=patient)
        try:
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    f'Patient {patient} updated successfully!'
                )
                return redirect('patient_list')
            else:
                messages.error(request, 'Please fix the errors below.')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
    else:
        # Pre-fill form with existing patient data
        form = PatientForm(instance=patient)

    return render(request, 'patients/form.html', {
        'form'   : form,
        'patient': patient,
        'action' : 'Edit Patient'
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = str(patient)
        patient.delete()
        messages.success(request, f'Patient {name} deleted successfully.')
        return redirect('patient_list')
    return render(request, 'patients/confirm_delete.html', {
        'patient': patient
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    # Get all appointments for this patient
    appointments = patient.appointments.all().order_by('-appointment_date')
    return render(request, 'patients/detail.html', {
        'patient'     : patient,
        'appointments': appointments
    })