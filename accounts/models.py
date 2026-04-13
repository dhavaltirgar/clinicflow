from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Role choices — using a tuple (immutable, perfect for fixed choices)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
    )

    # Extra fields on top of Django's default User
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # String representation — what shows in admin panel
    def __str__(self):
        return f"{self.username} ({self.role})"

    # Helper methods using built-in property decorator
    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'
    
# 💡 What is AbstractUser? Django already has a built-in User model with username, password, email
#   etc.Instead of building from scratch, we extend it and add our own fields (role, phone). This 
#   saves hours of work and is the professional way to do it.