from django.db import models
from django.conf import settings
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # Many-to-One: many appointments → one patient
    patient         = models.ForeignKey(
                        Patient,
                        on_delete=models.CASCADE,
                        related_name='appointments'
                      )
    # Many-to-One: many appointments → one doctor
    doctor          = models.ForeignKey(
                        Doctor,
                        on_delete=models.CASCADE,
                        related_name='appointments'
                      )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason          = models.TextField()
    notes           = models.TextField(blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} with Dr.{self.doctor.user.last_name} on {self.appointment_date}"

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        # Prevent double booking — same doctor can't have 2 appointments at same time
        unique_together = ['doctor', 'appointment_date', 'appointment_time']