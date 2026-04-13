from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display  = ('appointment', 'diagnosis', 'follow_up_date', 'created_at')
    search_fields = ('appointment__patient__first_name', 'diagnosis')
    ordering      = ('-created_at',)