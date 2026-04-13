from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prescription
from .forms import PrescriptionForm
from appointments.models import Appointment

# Import our custom decorator!
from accounts.decorators import doctor_required


# -------------------------------------------------------
# Only DOCTORS can write prescriptions
# Using our custom @doctor_required decorator
# -------------------------------------------------------
@login_required
@doctor_required
def prescription_add(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check if prescription already exists for this appointment
    if hasattr(appointment, 'prescription'):
        messages.warning(
            request,
            'Prescription already exists for this appointment.'
        )
        return redirect(
            'prescription_detail',
            pk=appointment.prescription.pk
        )

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        try:
            if form.is_valid():
                prescription = form.save()

                # Mark appointment as completed
                appointment.status = 'completed'
                appointment.save()

                messages.success(
                    request,
                    'Prescription written successfully!'
                )
                return redirect(
                    'prescription_detail',
                    pk=prescription.pk
                )
            else:
                messages.error(request, 'Please fix the errors below.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        # Pre-select the appointment in the form
        form = PrescriptionForm(
            initial={'appointment': appointment}
        )

    return render(request, 'prescriptions/form.html', {
        'form'       : form,
        'appointment': appointment,
        'action'     : 'Write Prescription'
    })


@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    # Lambda function — get medicine list from PDF!
    medicine_list = list(
        map(
            lambda m: m.strip(),
            prescription.medicines.split(',')
        )
    )

    return render(request, 'prescriptions/detail.html', {
        'prescription' : prescription,
        'medicine_list': medicine_list,
    })


@login_required
def prescription_list(request):
    # Doctors see only their prescriptions
    # Admin/receptionist see all
    if request.user.role == 'doctor':
        prescriptions = Prescription.objects.filter(
            appointment__doctor__user=request.user
        ).select_related('appointment__patient')
    else:
        prescriptions = Prescription.objects.select_related(
            'appointment__patient',
            'appointment__doctor__user'
        ).all()

    return render(request, 'prescriptions/list.html', {
        'prescriptions': prescriptions
    })