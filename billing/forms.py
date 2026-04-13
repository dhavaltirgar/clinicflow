from django import forms
from .models import Bill


class BillForm(forms.ModelForm):

    class Meta:
        model  = Bill
        fields = [
            'appointment', 'patient',
            'consultation_fee', 'medicine_charges', 'other_charges',
            'payment_status', 'payment_method'
        ]
        widgets = {
            'appointment'     : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
            'patient'         : forms.Select(attrs={
                                  'class': 'form-control'
                                }),

            # ---- Fee fields — proper decimal inputs ----
            'consultation_fee': forms.NumberInput(attrs={
                                  'class'      : 'form-control',
                                  'step'       : '0.01',  # allows 500.00, 250.50
                                  'min'        : '0',
                                  'placeholder': '0.00'
                                }),
            'medicine_charges': forms.NumberInput(attrs={
                                  'class'      : 'form-control',
                                  'step'       : '0.01',
                                  'min'        : '0',
                                  'placeholder': '0.00'
                                }),
            'other_charges'   : forms.NumberInput(attrs={
                                  'class'      : 'form-control',
                                  'step'       : '0.01',
                                  'min'        : '0',
                                  'placeholder': '0.00'
                                }),
            'payment_status'  : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
            'payment_method'  : forms.Select(attrs={
                                  'class': 'form-control'
                                }),
        }

    # Validate consultation fee — required, no negative
    def clean_consultation_fee(self):
        fee = self.cleaned_data.get('consultation_fee')
        if fee is None:
            raise forms.ValidationError(
                'Consultation fee is required.'
            )
        if fee < 0:
            raise forms.ValidationError(
                'Consultation fee cannot be negative.'
            )
        return fee

    # Validate medicine charges
    def clean_medicine_charges(self):
        charges = self.cleaned_data.get('medicine_charges')
        if charges and charges < 0:
            raise forms.ValidationError(
                'Medicine charges cannot be negative.'
            )
        return charges or 0

    # Validate other charges
    def clean_other_charges(self):
        charges = self.cleaned_data.get('other_charges')
        if charges and charges < 0:
            raise forms.ValidationError(
                'Other charges cannot be negative.'
            )
        return charges or 0