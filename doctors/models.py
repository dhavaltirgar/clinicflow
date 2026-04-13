from django.db import models
from django.conf import settings

class Doctor(models.Model):
    # One-to-One with User — one user account = one doctor profile
    user            = models.OneToOneField(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='doctor_profile'
                      )
    specialization  = models.CharField(max_length=100)
    qualification   = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    photo           = models.ImageField(upload_to='doctors/', blank=True, null=True)
    is_available    = models.BooleanField(default=True)
    bio             = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} — {self.specialization}"

    class Meta:
        ordering = ['specialization']