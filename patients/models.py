from django.db import models
import re  # Regular expressions — from your PDF!

class Patient(models.Model):
    # Gender choices stored as a tuple
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    )

    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)

    # Both email and phone are Candidate Keys — either uniquely identifies a patient
    email           = models.EmailField(unique=True)
    phone           = models.CharField(max_length=15, unique=True)

    date_of_birth   = models.DateField()
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group     = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address         = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Using built-in property + DateTime module to calculate age
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year

    # Regular Expression — validate phone number format
    @staticmethod
    def validate_phone(phone):
        pattern = re.compile(r'^\+?1?\d{10,15}$')
        return bool(pattern.match(phone))

    class Meta:
        ordering = ['-created_at']  # newest patients first