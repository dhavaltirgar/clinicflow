from django import forms
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor


class AppointmentForm(forms.ModelForm):

    class Meta:
        model  = Appointment
        fields = [
            'patient', 'doctor', 'appointment_date',
            'appointment_time', 'reason', 'status', 'notes'
        ]
        widgets = {
            'patient'         : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
            'doctor'          : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
            'appointment_date': forms.DateInput(attrs={
                                  'class': 'form-control',
                                  'type' : 'date'
                                }),
            'appointment_time': forms.TimeInput(attrs={
                                  'class': 'form-control',
                                  'type' : 'time'
                                }),
            'reason'          : forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'rows' : 3,
                                  'placeholder': 'Reason for visit'
                                }),
            'status'          : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
            'notes'           : forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'rows' : 2,
                                  'placeholder': 'Additional notes'
                                }),
        }

    # Validation — appointment date cannot be in the past
    def clean_appointment_date(self):
        from datetime import date
        appt_date = self.cleaned_data.get('appointment_date')
        if appt_date and appt_date < date.today():
            raise forms.ValidationError(
                'Appointment date cannot be in the past!'
            )
        return appt_date

    # Validate no double booking
    def clean(self):
        cleaned_data = super().clean()
        doctor       = cleaned_data.get('doctor')
        appt_date    = cleaned_data.get('appointment_date')
        appt_time    = cleaned_data.get('appointment_time')

        if doctor and appt_date and appt_time:
            # Check if slot is already taken
            existing = Appointment.objects.filter(
                doctor           = doctor,
                appointment_date = appt_date,
                appointment_time = appt_time,
                status__in       = ['pending', 'confirmed']
            )
            # Exclude current instance when editing
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    'This doctor already has an appointment at this time!'
                )
        return cleaned_data