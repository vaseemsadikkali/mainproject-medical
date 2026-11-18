from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin (Full Control)'),
        ('staff', 'Staff / Doctor (Partial Control)'),
        ('patient', 'Patient / User (Basic Access)'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_staff_member(self):
        return self.role == 'staff'

    def is_patient(self):
        return self.role == 'patient'

    def get_role_badge_class(self):
        if self.role == 'admin' or self.is_superuser:
            return 'bg-danger'
        elif self.role == 'staff':
            return 'bg-info text-dark'
        return 'bg-success'

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"


class PatientProfile(models.Model):
    BLOOD_GROUPS = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True, help_text="Past illnesses, surgeries, chronic conditions")
    allergies = models.TextField(blank=True, null=True, help_text="Drug or food allergies")

    def __str__(self):
        return f"Patient Profile: {self.user.username}"
