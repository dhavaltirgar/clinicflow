from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'gender', 'blood_group', 'created_at')
    list_filter = ('gender', 'blood_group')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)