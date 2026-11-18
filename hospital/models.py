from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi-hospital', help_text="Bootstrap icon class name, e.g., bi-heart-pulse")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    specialization = models.CharField(max_length=150)
    qualification = models.CharField(max_length=150)
    experience_years = models.PositiveIntegerField(default=1)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    room_number = models.CharField(max_length=20, default='101')
    available_days = models.CharField(max_length=100, default='Mon - Fri')
    available_time_slot = models.CharField(max_length=100, default='09:00 AM - 05:00 PM')
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        dept = f" ({self.department.name})" if self.department else ""
        return f"Dr. {full_name}{dept}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_for_visit = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    doctor_notes = models.TextField(blank=True, help_text="Notes added by attending doctor or staff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def get_status_badge(self):
        badges = {
            'pending': 'bg-warning text-dark',
            'confirmed': 'bg-primary text-white',
            'completed': 'bg-success text-white',
            'cancelled': 'bg-danger text-white',
        }
        return badges.get(self.status, 'bg-secondary')

    def __str__(self):
        return f"Apt #{self.id}: {self.patient.username} with {self.doctor} on {self.appointment_date}"


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records_issued')
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescribed_medicines = models.TextField()
    treatment_notes = models.TextField(blank=True)
    lab_report_file = models.FileField(upload_to='medical_reports/', blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Record #{self.id} for {self.patient.username} ({self.created_at.strftime('%Y-%m-%d')})"


class BillingInvoice(models.Model):
    PAYMENT_STATUS = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    )
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Debit / Credit Card'),
        ('upi', 'UPI / Online Payment'),
        ('insurance', 'Health Insurance'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=40, unique=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    medicine_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        if not self.total_amount:
            self.total_amount = self.consultation_fee + self.medicine_charges
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient.username} (${self.total_amount})"
