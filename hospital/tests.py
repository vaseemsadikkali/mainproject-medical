from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import time, timedelta
from decimal import Decimal

from accounts.models import User, PatientProfile
from hospital.models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


class RoleAccessAndCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Admin
        self.admin = User.objects.create_user(
            username='test_admin',
            password='password123',
            role='admin',
            is_staff=True,
            is_superuser=True
        )

        # Create Doctor
        self.doctor_user = User.objects.create_user(
            username='test_doctor',
            password='password123',
            role='staff',
            is_staff=True
        )
        self.dept = Department.objects.create(name='Cardiology', description='Heart care')
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            department=self.dept,
            specialization='Cardiologist',
            qualification='MBBS, MD',
            consultation_fee=Decimal('100.00'),
            room_number='101'
        )

        # Create Patient
        self.patient = User.objects.create_user(
            username='test_patient',
            password='password123',
            role='patient'
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient,
            blood_group='O+'
        )

    def test_role_properties(self):
        self.assertTrue(self.admin.is_admin())
        self.assertTrue(self.doctor_user.is_staff_member())
        self.assertTrue(self.patient.is_patient())

    def test_admin_dashboard_security_restriction(self):
        # Patient cannot access admin dashboard
        self.client.login(username='test_patient', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

        # Doctor cannot access admin dashboard
        self.client.login(username='test_doctor', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

        # Admin CAN access admin dashboard
        self.client.login(username='test_admin', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_doctor_dashboard_security(self):
        # Patient cannot access doctor dashboard
        self.client.login(username='test_patient', password='password123')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 302)

        # Doctor CAN access doctor dashboard
        self.client.login(username='test_doctor', password='password123')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_full_crud(self):
        # 1. CREATE: Patient books an appointment
        self.client.login(username='test_patient', password='password123')
        today = timezone.localdate() + timedelta(days=2)
        response = self.client.post(reverse('appointment_book'), {
            'department': self.dept.id,
            'doctor': self.doctor.id,
            'appointment_date': today,
            'appointment_time': '10:00',
            'reason_for_visit': 'General consultation and checkup',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)
        
        apt = Appointment.objects.first()
        self.assertEqual(apt.patient, self.patient)
        self.assertEqual(apt.status, 'pending')
        # Check auto invoice creation
        self.assertTrue(hasattr(apt, 'invoice'))
        self.assertEqual(apt.invoice.total_amount, Decimal('100.00'))

        # 2. READ: Read appointment list and detail
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cardiology')

        response = self.client.get(reverse('appointment_detail', args=[apt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'General consultation')

        # 3. UPDATE: Patient reschedules pending appointment
        reschedule_date = today + timedelta(days=1)
        response = self.client.post(reverse('appointment_edit', args=[apt.id]), {
            'department': self.dept.id,
            'doctor': self.doctor.id,
            'appointment_date': reschedule_date,
            'appointment_time': '11:00',
            'reason_for_visit': 'Updated reason: rescheduled checkup',
        })
        self.assertEqual(response.status_code, 302)
        apt.refresh_from_db()
        self.assertEqual(apt.appointment_date, reschedule_date)
        self.assertEqual(apt.reason_for_visit, 'Updated reason: rescheduled checkup')

        # Doctor updates appointment status
        self.client.login(username='test_doctor', password='password123')
        response = self.client.post(reverse('appointment_status_update', args=[apt.id]), {
            'status': 'confirmed',
            'doctor_notes': 'Confirmed with doctor',
        })
        self.assertEqual(response.status_code, 302)
        apt.refresh_from_db()
        self.assertEqual(apt.status, 'confirmed')

        # 4. DELETE / CANCEL: Admin deletes appointment
        self.client.login(username='test_admin', password='password123')
        response = self.client.post(reverse('appointment_delete', args=[apt.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_medical_record_creation(self):
        # Create an appointment
        apt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            department=self.dept,
            appointment_date=timezone.localdate(),
            appointment_time=time(14, 0),
            reason_for_visit='High blood pressure symptoms',
            status='confirmed'
        )

        # Doctor issues medical record
        self.client.login(username='test_doctor', password='password123')
        response = self.client.post(reverse('medical_record_create', args=[apt.id]), {
            'symptoms': 'Headache, fatigue',
            'diagnosis': 'Primary Hypertension',
            'treatment_notes': 'Dietary sodium reduction',
            'prescribed_medicines': 'Amlodipine 5mg once daily',
        })
        self.assertEqual(response.status_code, 302)

        # Verify medical record created and appointment marked completed
        apt.refresh_from_db()
        self.assertEqual(apt.status, 'completed')
        self.assertTrue(hasattr(apt, 'medical_record'))
        self.assertEqual(apt.medical_record.diagnosis, 'Primary Hypertension')
