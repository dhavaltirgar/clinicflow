from django.db import models
from appointments.models import Appointment

class Prescription(models.Model):
    # One-to-One: one appointment = one prescription
    appointment     = models.OneToOneField(
                        Appointment,
                        on_delete=models.CASCADE,
                        related_name='prescription'
                      )
    diagnosis       = models.TextField()
    medicines       = models.TextField()  # stored as text, processed with lambda later
    instructions    = models.TextField(blank=True)
    follow_up_date  = models.DateField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient}"

    # Lambda function — get list of medicines
    def get_medicine_list(self):
        return list(map(lambda m: m.strip(), self.medicines.split(',')))