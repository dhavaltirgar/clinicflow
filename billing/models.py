from django.db import models
from appointments.models import Appointment
from patients.models import Patient
import uuid


class Bill(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
    )
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    )

    # One-to-One: one appointment = one bill
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='bill'
    )
    # Many-to-One: one patient can have many bills
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    invoice_number    = models.CharField(max_length=20, unique=True, blank=True)
    consultation_fee  = models.DecimalField(max_digits=8, decimal_places=2)
    medicine_charges  = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    other_charges     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount      = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status    = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method    = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.id} — {self.patient} — ₹{self.total_amount}"

    # Built-in sum() function — calculate total automatically
    def calculate_total(self):
        charges = [self.consultation_fee, self.medicine_charges, self.other_charges]
        return sum(charges)

    # Auto generate invoice number + calculate total on save
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']