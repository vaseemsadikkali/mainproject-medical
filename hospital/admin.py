from django.contrib import admin
from .models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialization', 'experience_years', 'consultation_fee', 'room_number', 'is_available')
    list_filter = ('department', 'is_available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization', 'qualification')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'department', 'appointment_date')
    search_fields = ('patient__username', 'patient__first_name', 'doctor__user__first_name', 'reason_for_visit')
    date_hierarchy = 'appointment_date'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'patient', 'doctor', 'diagnosis', 'created_at')
    search_fields = ('patient__username', 'doctor__user__username', 'diagnosis', 'prescribed_medicines')
    date_hierarchy = 'created_at'


@admin.register(BillingInvoice)
class BillingInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'appointment', 'patient', 'total_amount', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('invoice_number', 'patient__username')
    date_hierarchy = 'created_at'
