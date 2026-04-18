from django import forms
from .models import Prescription
from appointments.models import Appointment
from django.utils import timezone   


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model  = Prescription
        fields = [
            'appointment', 'diagnosis',
            'medicines', 'instructions', 'follow_up_date'
        ]
        widgets = {
            'appointment' : forms.Select(attrs={
                              'class': 'form-control'
                            }),
            'diagnosis'   : forms.Textarea(attrs={
                              'class'      : 'form-control',
                              'rows'       : 4,
                              'placeholder': 'Enter diagnosis details...'
                            }),
            'medicines'   : forms.Textarea(attrs={
                              'class'      : 'form-control',
                              'rows'       : 4,
                              'placeholder': 'Enter medicines separated by commas\nExample: Paracetamol 500mg, Amoxicillin 250mg'
                            }),
            'instructions': forms.Textarea(attrs={
                              'class'      : 'form-control',
                              'rows'       : 3,
                              'placeholder': 'Enter instructions for patient...'
                            }),
            'follow_up_date': forms.DateInput(attrs={
                              'class': 'form-control',
                              'type' : 'date',
                              'min'  : timezone.now().date().strftime('%Y-%m-%d')
                            }),
        }

    # Diagnosis cannot be empty
    def clean_diagnosis(self):
        diagnosis = self.cleaned_data.get('diagnosis')
        if len(diagnosis.strip()) < 10:
            raise forms.ValidationError(
                'Diagnosis must be at least 10 characters long.'
            )
        return diagnosis.strip()

    # Medicines — Lambda function used here
    def clean_medicines(self):
        medicines = self.cleaned_data.get('medicines')
        if not medicines.strip():
            raise forms.ValidationError(
                'Please enter at least one medicine.'
            )
        # Clean each medicine name using Lambda — from your PDF!
        medicine_list = list(
            filter(
                lambda m: m.strip(),
                medicines.split(',')
            )
        )
        if len(medicine_list) == 0:
            raise forms.ValidationError('Please enter valid medicine names.')
        # Return cleaned comma-separated string
        return ', '.join(medicine_list)
    
    # Follow up date must be in the future
    def clean_follow_up_date(self):
        follow_up_date = self.cleaned_data.get('follow_up_date')

        if follow_up_date:
            if follow_up_date <= timezone.now().date():
                raise forms.ValidationError(
                    "Follow-up date must be a future date!"
                )

        return follow_up_date