from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
import json
from decimal import Decimal

from accounts.models import User
from accounts.decorators import admin_required, staff_or_admin_required, role_required
from .models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice
from .forms import (
    AppointmentBookingForm, AppointmentUpdateForm, AppointmentStatusUpdateForm,
    MedicalRecordForm, DepartmentForm, DoctorForm, BillingInvoiceForm
)


# ==========================================
# 1. PUBLIC VIEWS & LANDING PAGE
# ==========================================

def home_view(request):
    departments = Department.objects.filter(is_active=True)[:6]
    doctors = Doctor.objects.filter(is_available=True).select_related('user', 'department')[:6]
    
    total_doctors = Doctor.objects.filter(is_available=True).count()
    total_departments = Department.objects.filter(is_active=True).count()
    total_patients = User.objects.filter(role='patient').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()

    context = {
        'departments': departments,
        'doctors': doctors,
        'total_doctors': total_doctors,
        'total_departments': total_departments,
        'total_patients': total_patients,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'hospital/home.html', context)


def doctors_list_view(request):
    query = request.GET.get('q', '').strip()
    dept_id = request.GET.get('department', '').strip()

    doctors = Doctor.objects.filter(is_available=True).select_related('user', 'department')
    departments = Department.objects.filter(is_active=True)

    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(qualification__icontains=query)
        )
    if dept_id:
        doctors = doctors.filter(department_id=dept_id)

    context = {
        'doctors': doctors,
        'departments': departments,
        'query': query,
        'selected_dept': dept_id,
    }
    return render(request, 'hospital/doctors_list.html', context)


def doctor_detail_view(request, doctor_id):
    doctor = get_object_or_404(Doctor.objects.select_related('user', 'department'), id=doctor_id)
    return render(request, 'hospital/doctor_detail.html', {'doctor': doctor})


def departments_list_view(request):
    departments = Department.objects.filter(is_active=True).annotate(doctor_count=Count('doctors'))
    return render(request, 'hospital/department_list.html', {'departments': departments})


# ==========================================
# 2. ROLE-BASED DASHBOARDS
# ==========================================

@admin_required
def admin_dashboard_view(request):
    today = timezone.localdate()
    
    total_users = User.objects.count()
    total_patients = User.objects.filter(role='patient').count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    cancelled_appointments = Appointment.objects.filter(status='cancelled').count()
    
    total_revenue_dict = BillingInvoice.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))
    total_revenue = total_revenue_dict['total'] or Decimal('0.00')

    # Department stats
    dept_stats = Department.objects.annotate(apt_count=Count('appointments')).order_by('-apt_count')[:6]
    dept_labels = [d.name for d in dept_stats]
    dept_counts = [d.apt_count for d in dept_stats]

    # Status distribution
    status_labels = ['Pending', 'Confirmed', 'Completed', 'Cancelled']
    status_counts = [pending_appointments, confirmed_appointments, completed_appointments, cancelled_appointments]

    # Recent appointments
    recent_appointments = Appointment.objects.select_related('patient', 'doctor__user', 'department').order_by('-created_at')[:8]

    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'total_revenue': total_revenue,
        'dept_labels_json': json.dumps(dept_labels),
        'dept_counts_json': json.dumps(dept_counts),
        'status_labels_json': json.dumps(status_labels),
        'status_counts_json': json.dumps(status_counts),
        'recent_appointments': recent_appointments,
    }
    return render(request, 'hospital/dashboard_admin.html', context)


@staff_or_admin_required
def doctor_dashboard_view(request):
    today = timezone.localdate()
    user = request.user

    # Find doctor profile
    doctor = getattr(user, 'doctor_profile', None)
    if not doctor and user.is_admin():
        # Admin can view all or fallback to first doctor for test view
        doctor = Doctor.objects.first()

    if not doctor:
        messages.warning(request, "No doctor profile associated with this account. Please create one.")
        return redirect('admin_dashboard')

    doctor_appointments = Appointment.objects.filter(doctor=doctor).select_related('patient', 'department')
    today_appointments = doctor_appointments.filter(appointment_date=today).order_by('appointment_time')
    upcoming_appointments = doctor_appointments.filter(appointment_date__gte=today).exclude(status__in=['completed', 'cancelled']).order_by('appointment_date', 'appointment_time')[:10]
    
    total_consulted = doctor_appointments.filter(status='completed').count()
    pending_count = doctor_appointments.filter(status='pending').count()
    today_count = today_appointments.count()

    context = {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'total_consulted': total_consulted,
        'pending_count': pending_count,
        'today_count': today_count,
    }
    return render(request, 'hospital/dashboard_doctor.html', context)


@login_required
def patient_dashboard_view(request):
    if not request.user.is_patient() and not request.user.is_admin():
        return redirect('dashboard_redirect')

    user = request.user
    appointments = Appointment.objects.filter(patient=user).select_related('doctor__user', 'department').order_by('-appointment_date', '-appointment_time')
    upcoming_appointments = appointments.filter(appointment_date__gte=timezone.localdate()).exclude(status__in=['completed', 'cancelled'])
    past_appointments = appointments.filter(Q(appointment_date__lt=timezone.localdate()) | Q(status__in=['completed', 'cancelled']))[:10]
    
    records = MedicalRecord.objects.filter(patient=user).select_related('doctor__user', 'appointment').order_by('-created_at')[:5]
    invoices = BillingInvoice.objects.filter(patient=user).select_related('appointment').order_by('-created_at')[:5]

    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'records': records,
        'invoices': invoices,
        'total_appointments': appointments.count(),
    }
    return render(request, 'hospital/dashboard_patient.html', context)


# ==========================================
# 3. APPOINTMENT CRUD OPERATIONS (Full CRUD)
# ==========================================

# CREATE
@login_required
def appointment_book_view(request):
    initial_data = {}
    dept_id = request.GET.get('department')
    doc_id = request.GET.get('doctor')
    if dept_id:
        initial_data['department'] = dept_id
    if doc_id:
        initial_data['doctor'] = doc_id

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'pending'
            appointment.save()

            # Auto-generate Billing Invoice
            fee = appointment.doctor.consultation_fee
            BillingInvoice.objects.create(
                appointment=appointment,
                patient=request.user,
                consultation_fee=fee,
                medicine_charges=Decimal('0.00'),
                total_amount=fee,
                payment_status='unpaid',
                payment_method='cash'
            )

            messages.success(request, f"Appointment successfully booked with {appointment.doctor} for {appointment.appointment_date} at {appointment.appointment_time}!")
            return redirect('appointment_detail', appointment_id=appointment.id)
        else:
            messages.error(request, "Failed to book appointment. Please review errors.")
    else:
        form = AppointmentBookingForm(initial=initial_data)

    return render(request, 'hospital/book_appointment.html', {'form': form})


# READ (List & Search & Filter)
@login_required
def appointment_list_view(request):
    user = request.user
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    date_filter = request.GET.get('date', '').strip()

    if user.is_admin():
        appointments = Appointment.objects.all().select_related('patient', 'doctor__user', 'department')
    elif user.is_staff_member():
        doctor = getattr(user, 'doctor_profile', None)
        appointments = Appointment.objects.filter(doctor=doctor).select_related('patient', 'doctor__user', 'department') if doctor else Appointment.objects.none()
    else:
        appointments = Appointment.objects.filter(patient=user).select_related('doctor__user', 'department')

    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(doctor__user__first_name__icontains=query) |
            Q(doctor__user__last_name__icontains=query) |
            Q(reason_for_visit__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)

    context = {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    return render(request, 'hospital/appointment_list.html', context)


# READ (Detail)
@login_required
def appointment_detail_view(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor__user', 'department'),
        id=appointment_id
    )

    # Permission check: Admin, attending Doctor, or booking Patient
    is_doctor = hasattr(request.user, 'doctor_profile') and request.user.doctor_profile == appointment.doctor
    if not (request.user.is_admin() or is_doctor or request.user == appointment.patient):
        messages.error(request, "You are not authorized to view this appointment.")
        return redirect('dashboard_redirect')

    medical_record = getattr(appointment, 'medical_record', None)
    invoice = getattr(appointment, 'invoice', None)

    context = {
        'appointment': appointment,
        'medical_record': medical_record,
        'invoice': invoice,
        'is_doctor': is_doctor,
    }
    return render(request, 'hospital/appointment_detail.html', context)


# UPDATE (Reschedule / Edit)
@login_required
def appointment_edit_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Patient can only edit their own appointment if it's pending; Admin can always edit
    if not (request.user.is_admin() or (request.user == appointment.patient and appointment.status == 'pending')):
        messages.error(request, "You cannot edit this appointment.")
        return redirect('appointment_detail', appointment_id=appointment.id)

    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentUpdateForm(instance=appointment)

    return render(request, 'hospital/appointment_edit.html', {'form': form, 'appointment': appointment})


# UPDATE (Status by Doctor or Admin)
@staff_or_admin_required
def appointment_status_update_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    is_doctor = hasattr(request.user, 'doctor_profile') and request.user.doctor_profile == appointment.doctor

    if not (request.user.is_admin() or is_doctor):
        messages.error(request, "You do not have permission to change this appointment's status.")
        return redirect('appointment_detail', appointment_id=appointment.id)

    if request.method == 'POST':
        form = AppointmentStatusUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Appointment status changed to '{appointment.get_status_display()}'!")
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentStatusUpdateForm(instance=appointment)

    return render(request, 'hospital/appointment_status_update.html', {'form': form, 'appointment': appointment})


# DELETE (Cancel / Delete)
@login_required
def appointment_delete_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Permission check: Patient can cancel if pending; Admin can delete any
    can_delete = request.user.is_admin() or (request.user == appointment.patient and appointment.status in ['pending', 'confirmed'])
    if not can_delete:
        messages.error(request, "You cannot cancel or delete this appointment.")
        return redirect('appointment_detail', appointment_id=appointment.id)

    if request.method == 'POST':
        if request.user.is_admin():
            appointment.delete()
            messages.success(request, "Appointment was deleted permanently.")
            return redirect('appointment_list')
        else:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, "Your appointment has been cancelled.")
            return redirect('patient_dashboard')

    return render(request, 'hospital/appointment_confirm_delete.html', {'appointment': appointment})


# ==========================================
# 4. MEDICAL RECORDS (CRUD)
# ==========================================

@staff_or_admin_required
def medical_record_create_view(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor'), id=appointment_id)

    if hasattr(appointment, 'medical_record'):
        messages.info(request, "A medical record already exists for this appointment. You may edit it below.")
        return redirect('medical_record_edit', record_id=appointment.medical_record.id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.appointment = appointment
            record.patient = appointment.patient
            record.doctor = appointment.doctor
            record.save()

            # Mark appointment as completed
            appointment.status = 'completed'
            appointment.save()

            messages.success(request, f"Medical record & prescription created for {appointment.patient.username}!")
            return redirect('medical_record_detail', record_id=record.id)
    else:
        form = MedicalRecordForm()

    return render(request, 'hospital/medical_record_form.html', {'form': form, 'appointment': appointment})


@login_required
def medical_record_detail_view(request, record_id):
    record = get_object_or_404(
        MedicalRecord.objects.select_related('patient', 'doctor__user', 'appointment__department'),
        id=record_id
    )

    # Permission check: Patient, assigned Doctor, or Admin
    is_doctor = hasattr(request.user, 'doctor_profile') and request.user.doctor_profile == record.doctor
    if not (request.user.is_admin() or is_doctor or request.user == record.patient):
        messages.error(request, "You are not authorized to view this medical record.")
        return redirect('dashboard_redirect')

    return render(request, 'hospital/medical_record_detail.html', {'record': record})


@staff_or_admin_required
def medical_record_edit_view(request, record_id):
    record = get_object_or_404(MedicalRecord.objects.select_related('appointment', 'patient'), id=record_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical record updated successfully!")
            return redirect('medical_record_detail', record_id=record.id)
    else:
        form = MedicalRecordForm(instance=record)

    return render(request, 'hospital/medical_record_form.html', {'form': form, 'appointment': record.appointment, 'record': record})


# ==========================================
# 5. DEPARTMENT MANAGEMENT (ADMIN CRUD)
# ==========================================

@admin_required
def department_create_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f"Department '{dept.name}' created successfully!")
            return redirect('departments_list')
    else:
        form = DepartmentForm()
    return render(request, 'hospital/department_form.html', {'form': form, 'title': 'Create New Department'})


@admin_required
def department_edit_view(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Department '{dept.name}' updated successfully!")
            return redirect('departments_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'hospital/department_form.html', {'form': form, 'dept': dept, 'title': f"Edit {dept.name}"})


@admin_required
def department_delete_view(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == 'POST':
        name = dept.name
        dept.delete()
        messages.success(request, f"Department '{name}' deleted successfully.")
        return redirect('departments_list')
    return render(request, 'hospital/department_confirm_delete.html', {'dept': dept})


# ==========================================
# 6. DOCTOR MANAGEMENT (ADMIN CRUD)
# ==========================================

@admin_required
def doctor_create_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        user_id = request.POST.get('user_id')
        if form.is_valid() and user_id:
            user = get_object_or_404(User, id=user_id)
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            user.role = 'staff'
            user.save()
            messages.success(request, f"Doctor profile for {user.username} created!")
            return redirect('doctors_list')
    else:
        form = DoctorForm()

    available_users = User.objects.filter(role__in=['staff', 'admin'], doctor_profile__isnull=True)
    return render(request, 'hospital/doctor_form.html', {'form': form, 'available_users': available_users, 'title': 'Add Doctor Profile'})


@admin_required
def doctor_edit_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doctor {doctor} updated successfully!")
            return redirect('doctors_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor_form.html', {'form': form, 'doctor': doctor, 'title': f"Edit Doctor: {doctor}"})


# ==========================================
# 7. BILLING & INVOICES
# ==========================================

@login_required
def invoice_detail_view(request, invoice_id):
    invoice = get_object_or_404(BillingInvoice.objects.select_related('appointment__doctor__user', 'patient'), id=invoice_id)

    # Permission check: patient or staff/admin
    if not (request.user.is_admin() or request.user.is_staff_member() or request.user == invoice.patient):
        messages.error(request, "You are not authorized to view this invoice.")
        return redirect('dashboard_redirect')

    return render(request, 'hospital/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_pay_view(request, invoice_id):
    invoice = get_object_or_404(BillingInvoice, id=invoice_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')
        invoice.payment_method = payment_method
        invoice.payment_status = 'paid'
        invoice.paid_at = timezone.now()
        invoice.save()
        messages.success(request, f"Invoice #{invoice.invoice_number} paid successfully!")
        return redirect('invoice_detail', invoice_id=invoice.id)

    return render(request, 'hospital/invoice_pay.html', {'invoice': invoice})


# ==========================================
# 8. REPORTS & ANALYTICS
# ==========================================

@admin_required
def reports_view(request):
    dept_id = request.GET.get('department')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    appointments = Appointment.objects.select_related('patient', 'doctor__user', 'department')
    if dept_id:
        appointments = appointments.filter(department_id=dept_id)
    if start_date:
        appointments = appointments.filter(appointment_date__gte=start_date)
    if end_date:
        appointments = appointments.filter(appointment_date__lte=end_date)

    total_count = appointments.count()
    completed_count = appointments.filter(status='completed').count()
    cancelled_count = appointments.filter(status='cancelled').count()
    
    invoices = BillingInvoice.objects.filter(appointment__in=appointments)
    revenue = invoices.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    departments = Department.objects.all()

    context = {
        'appointments': appointments.order_by('-appointment_date')[:50],
        'departments': departments,
        'total_count': total_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'revenue': revenue,
        'selected_dept': dept_id,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'hospital/reports.html', context)
