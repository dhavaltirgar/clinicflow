from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'specialization', 'qualification', 'experience_years', 'consultation_fee', 'is_available')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')