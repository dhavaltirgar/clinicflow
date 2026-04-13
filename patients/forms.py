from django import forms
from .models import Patient
import re
from datetime import date


class PatientForm(forms.ModelForm):

    class Meta:
        model  = Patient
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'blood_group',
            'address', 'medical_history'
        ]
        widgets = {
            'first_name'     : forms.TextInput(attrs={
                                'class'      : 'form-control',
                                'placeholder': 'Enter first name'
                               }),
            'last_name'      : forms.TextInput(attrs={
                                'class'      : 'form-control',
                                'placeholder': 'Enter last name'
                               }),
            'email'          : forms.EmailInput(attrs={
                                'class'      : 'form-control',
                                'placeholder': 'Enter email address'
                               }),
            'phone'          : forms.TextInput(attrs={
                                'class'      : 'form-control',
                                'placeholder': 'Enter 10 digit phone number',
                                'maxlength'  : '10',   # max 10 characters
                                'minlength'  : '10',   # min 10 characters
                                'pattern'    : '[0-9]{10}', # only numbers HTML level
                                'inputmode'  : 'numeric',   # shows number keyboard on mobile
                               }),
            'date_of_birth'  : forms.DateInput(attrs={
                                'class': 'form-control',
                                'type' : 'date',
                                'max'  : date.today().strftime('%Y-%m-%d'), # can't select future date
                                'min'  : '1900-01-01',  # reasonable minimum
                               }),
            'gender'         : forms.Select(attrs={
                                'class': 'form-control'
                               }),
            'blood_group'    : forms.Select(attrs={
                                'class': 'form-control'
                               }),
            'address'        : forms.Textarea(attrs={
                                'class'      : 'form-control',
                                'rows'       : 3,
                                'placeholder': 'Enter address'
                               }),
            'medical_history': forms.Textarea(attrs={
                                'class'      : 'form-control',
                                'rows'       : 4,
                                'placeholder': 'Enter medical history'
                               }),
        }

    # -------------------------------------------------------
    # Phone validation — only numbers, exactly 10 digits
    # -------------------------------------------------------
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Remove spaces if any
        phone = phone.strip()

        # Check only digits — no letters, no special chars
        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only numbers. No letters or special characters allowed.'
            )

        # Check exactly 10 digits
        if len(phone) != 10:
            raise forms.ValidationError(
                f'Phone number must be exactly 10 digits. You entered {len(phone)} digits.'
            )

        # Check doesn't start with 0
        if phone.startswith('0'):
            raise forms.ValidationError(
                'Phone number cannot start with 0.'
            )

        # Check unique — for new patients only
        if self.instance.pk is None:
            if Patient.objects.filter(phone=phone).exists():
                raise forms.ValidationError(
                    'A patient with this phone number already exists.'
                )

        return phone

    # -------------------------------------------------------
    # Date of birth validation — no future dates
    # -------------------------------------------------------
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')

        if dob:
            today = date.today()

            # Cannot be in the future
            if dob > today:
                raise forms.ValidationError(
                    'Date of birth cannot be in the future.'
                )

            # Cannot be more than 120 years ago
            age = today.year - dob.year
            if age > 120:
                raise forms.ValidationError(
                    'Please enter a valid date of birth.'
                )

            # Cannot be today (person can't be 0 days old)
            if dob == today:
                raise forms.ValidationError(
                    'Date of birth cannot be today.'
                )

        return dob

    # -------------------------------------------------------
    # Email validation
    # -------------------------------------------------------
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk is None:
            if Patient.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    'A patient with this email already exists.'
                )
        return email

    # -------------------------------------------------------
    # First name — no numbers allowed
    # -------------------------------------------------------
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError(
                'First name cannot contain numbers.'
            )
        return first_name.strip().title()

    # -------------------------------------------------------
    # Last name — no numbers allowed
    # -------------------------------------------------------
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError(
                'Last name cannot contain numbers.'
            )
        return last_name.strip().title()