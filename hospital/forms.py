from django import forms
from .models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['department', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select', 'id': 'id_department'}),
            'doctor': forms.Select(attrs={'class': 'form-select', 'id': 'id_doctor'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason_for_visit': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your symptoms or reason for visit...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True)
        self.fields['department'].queryset = Department.objects.filter(is_active=True)


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['department', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason_for_visit': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AppointmentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'doctor_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinical notes or instructions...'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['symptoms', 'diagnosis', 'treatment_notes', 'prescribed_medicines', 'lab_report_file', 'follow_up_date']
        widgets = {
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Patient symptoms reported...'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medical diagnosis...'}),
            'treatment_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Treatment procedures/recommendations...'}),
            'prescribed_medicines': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'e.g., Paracetamol 500mg - 1 tablet 3x daily after meals (5 days)...'}),
            'lab_report_file': forms.FileInput(attrs={'class': 'form-control'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'icon', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. bi-heart-pulse, bi-capsule, bi-lungs'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'department', 'specialization', 'qualification', 'experience_years',
            'consultation_fee', 'room_number', 'available_days', 'available_time_slot',
            'bio', 'is_available'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control'}),
            'available_time_slot': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BillingInvoiceForm(forms.ModelForm):
    class Meta:
        model = BillingInvoice
        fields = ['consultation_fee', 'medicine_charges', 'payment_status', 'payment_method']
        widgets = {
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'medicine_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
