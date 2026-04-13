from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'appointment', 'total_amount', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('patient__first_name', 'patient__last_name')