from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date, time
from decimal import Decimal

from accounts.models import User, PatientProfile
from hospital.models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


class Command(BaseCommand):
    help = 'Seeds database with sample roles, departments, doctors, appointments, medical records, and invoices'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting database seed..."))

        # 1. Create Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@medicarehub.org',
                'first_name': 'Alexander',
                'last_name': 'Wright',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+1 (555) 010-0001',
            }
        )
        admin_user.set_password('Admin@1234')
        admin_user.role = 'admin'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"Admin ready: {admin_user.username}"))

        # 2. Create Departments
        depts_data = [
            {
                'name': 'Cardiology',
                'icon': 'bi-heart-pulse',
                'description': 'Comprehensive cardiovascular care including ECG, echocardiogram, and coronary heart disease management.'
            },
            {
                'name': 'Neurology',
                'icon': 'bi-brain',
                'description': 'Specialized diagnosis and treatment of brain, spinal cord, and central nervous system disorders.'
            },
            {
                'name': 'Pediatrics',
                'icon': 'bi-emoji-smile',
                'description': 'Dedicated compassionate healthcare for infants, children, and adolescents.'
            },
            {
                'name': 'Orthopedics',
                'icon': 'bi-bandaid',
                'description': 'Treatment for musculoskeletal conditions, sports injuries, joint replacements, and bone health.'
            },
            {
                'name': 'Dermatology',
                'icon': 'bi-shield-plus',
                'description': 'Advanced medical and cosmetic skin care, allergy treatment, and dermatological therapies.'
            },
            {
                'name': 'General Medicine',
                'icon': 'bi-hospital',
                'description': 'Primary care, annual check-ups, preventative wellness, and chronic illness management.'
            },
        ]

        departments = {}
        for d_info in depts_data:
            dept, _ = Department.objects.get_or_create(
                name=d_info['name'],
                defaults={
                    'icon': d_info['icon'],
                    'description': d_info['description'],
                    'is_active': True,
                }
            )
            departments[d_info['name']] = dept
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(departments)} departments."))

        # 3. Create Doctors / Staff Users
        doctors_info = [
            {
                'username': 'dr_smith',
                'email': 'smith@medicarehub.org',
                'first_name': 'Robert',
                'last_name': 'Smith',
                'dept': 'Cardiology',
                'specialization': 'Senior Interventional Cardiologist',
                'qualification': 'MBBS, MD (Cardiology), FACC',
                'experience': 14,
                'fee': Decimal('150.00'),
                'room': '302-A',
                'bio': 'Dr. Robert Smith has over 14 years of clinical experience in interventional cardiology and preventative vascular medicine.'
            },
            {
                'username': 'dr_sarah',
                'email': 'sarah@medicarehub.org',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'dept': 'Pediatrics',
                'specialization': 'Consultant Pediatrician',
                'qualification': 'MBBS, DCH, MD (Pediatrics)',
                'experience': 9,
                'fee': Decimal('100.00'),
                'room': '104',
                'bio': 'Dr. Sarah Jenkins is renowned for her warm bedside manner with young children and expertise in pediatric developmental milestones.'
            },
            {
                'username': 'dr_emily',
                'email': 'emily@medicarehub.org',
                'first_name': 'Emily',
                'last_name': 'Chen',
                'dept': 'Neurology',
                'specialization': 'Clinical Neurologist',
                'qualification': 'MBBS, DM (Neurology)',
                'experience': 11,
                'fee': Decimal('180.00'),
                'room': '210-B',
                'bio': 'Dr. Emily Chen specializes in headache disorders, epilepsy management, and neurological rehabilitation.'
            },
            {
                'username': 'dr_marcus',
                'email': 'marcus@medicarehub.org',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'dept': 'Orthopedics',
                'specialization': 'Orthopedic & Joint Surgeon',
                'qualification': 'MBBS, MS (Ortho), MCh',
                'experience': 16,
                'fee': Decimal('160.00'),
                'room': '401',
                'bio': 'Specialist in minimally invasive arthroscopic surgery and sports joint rehabilitation.'
            }
        ]

        doctors = []
        for d in doctors_info:
            doc_user, _ = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'email': d['email'],
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'role': 'staff',
                    'is_staff': True,
                    'phone': '+1 (555) 012-3456',
                }
            )
            doc_user.set_password('Doctor@1234')
            doc_user.role = 'staff'
            doc_user.is_staff = True
            doc_user.save()

            doctor_obj, _ = Doctor.objects.get_or_create(
                user=doc_user,
                defaults={
                    'department': departments[d['dept']],
                    'specialization': d['specialization'],
                    'qualification': d['qualification'],
                    'experience_years': d['experience'],
                    'consultation_fee': d['fee'],
                    'room_number': d['room'],
                    'bio': d['bio'],
                    'is_available': True,
                }
            )
            doctors.append(doctor_obj)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(doctors)} doctors."))

        # 4. Create Patients
        patients_info = [
            {
                'username': 'john_doe',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+1 (555) 987-6543',
                'blood_group': 'O+',
                'allergies': 'Penicillin',
                'history': 'Hypertension diagnosed in 2021'
            },
            {
                'username': 'lisa_wong',
                'email': 'lisa.wong@example.com',
                'first_name': 'Lisa',
                'last_name': 'Wong',
                'phone': '+1 (555) 321-7654',
                'blood_group': 'A+',
                'allergies': 'None',
                'history': 'Mild seasonal asthma'
            },
            {
                'username': 'david_miller',
                'email': 'david.miller@example.com',
                'first_name': 'David',
                'last_name': 'Miller',
                'phone': '+1 (555) 456-7890',
                'blood_group': 'B-',
                'allergies': 'Sulfa drugs',
                'history': 'Previous meniscus repair (2023)'
            }
        ]

        patients = []
        for p in patients_info:
            p_user, _ = User.objects.get_or_create(
                username=p['username'],
                defaults={
                    'email': p['email'],
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'role': 'patient',
                    'phone': p['phone'],
                }
            )
            p_user.set_password('Patient@1234')
            p_user.role = 'patient'
            p_user.save()

            profile, _ = PatientProfile.objects.get_or_create(user=p_user)
            profile.blood_group = p['blood_group']
            profile.allergies = p['allergies']
            profile.medical_history = p['history']
            profile.emergency_contact_name = 'Mary ' + p['last_name']
            profile.emergency_contact_phone = '+1 (555) 000-9999'
            profile.save()

            patients.append(p_user)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(patients)} patients."))

        # 5. Create Sample Appointments & Medical Records & Invoices
        today = timezone.localdate()
        
        sample_appointments = [
            # 1. Today's confirmed appointment for Dr. Smith
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'dept': doctors[0].department,
                'date': today,
                'time': time(10, 30),
                'reason': 'Routine blood pressure review and mild chest tightness after exercise.',
                'status': 'confirmed',
                'notes': 'Patient advised to bring previous ECG readings.',
                'create_record': False,
                'paid': False,
            },
            # 2. Today's pending appointment for Dr. Sarah
            {
                'patient': patients[1],
                'doctor': doctors[1],
                'dept': doctors[1].department,
                'date': today,
                'time': time(14, 0),
                'reason': 'Annual developmental pediatric checkup and immunization update.',
                'status': 'pending',
                'notes': '',
                'create_record': False,
                'paid': False,
            },
            # 3. Completed past appointment with Dr. Emily
            {
                'patient': patients[0],
                'doctor': doctors[2],
                'dept': doctors[2].department,
                'date': today - timedelta(days=5),
                'time': time(11, 0),
                'reason': 'Recurring tension-type headaches and sleep disturbance.',
                'status': 'completed',
                'notes': 'Prescribed preventive medication and ergonomic posture guidance.',
                'create_record': True,
                'symptoms': 'Throbbing temporal headache, sensitivity to bright screen light, difficulty concentrating.',
                'diagnosis': 'Tension-Type Headache with Stress-Induced Insomnia',
                'rx': '1. Tab. Naproxen 250mg - 1 tablet as needed with food\n2. Tab. Magnesium Glycinate 400mg - 1 tablet at bedtime\n3. Melatonin 3mg - 1 tablet 30 min before sleep',
                'treatment_notes': 'Perform daily neck stretch exercises and reduce screen exposure 1 hour prior to sleep.',
                'follow_up': today + timedelta(days=25),
                'paid': True,
            },
            # 4. Completed past appointment with Dr. Smith
            {
                'patient': patients[1],
                'doctor': doctors[0],
                'dept': doctors[0].department,
                'date': today - timedelta(days=12),
                'time': time(9, 15),
                'reason': 'Palpitations and shortness of breath while climbing stairs.',
                'status': 'completed',
                'notes': 'Normal sinus rhythm, advised lifestyle modifications.',
                'create_record': True,
                'symptoms': 'Occasional rapid heartbeat episodes, dizziness after heavy exertion.',
                'diagnosis': 'Mild Benign Sinus Tachycardia',
                'rx': '1. Tab. Metoprolol Tartrate 25mg - 1 tablet daily morning after breakfast (30 days)\n2. Maintain daily hydration (>2.5 liters/day)',
                'treatment_notes': 'Limit excessive caffeine and energy drinks. Walk 30 minutes at a moderate pace daily.',
                'follow_up': today + timedelta(days=18),
                'paid': True,
            },
            # 5. Upcoming appointment next week with Dr. Marcus
            {
                'patient': patients[2],
                'doctor': doctors[3],
                'dept': doctors[3].department,
                'date': today + timedelta(days=4),
                'time': time(15, 30),
                'reason': 'Right knee pain when descending stairs.',
                'status': 'pending',
                'notes': '',
                'create_record': False,
                'paid': False,
            },
            # 6. Cancelled appointment
            {
                'patient': patients[2],
                'doctor': doctors[1],
                'dept': doctors[1].department,
                'date': today - timedelta(days=2),
                'time': time(16, 0),
                'reason': 'General wellness consultation.',
                'status': 'cancelled',
                'notes': 'Patient requested rescheduling due to travel.',
                'create_record': False,
                'paid': False,
            }
        ]

        for apt_data in sample_appointments:
            apt = Appointment.objects.create(
                patient=apt_data['patient'],
                doctor=apt_data['doctor'],
                department=apt_data['dept'],
                appointment_date=apt_data['date'],
                appointment_time=apt_data['time'],
                reason_for_visit=apt_data['reason'],
                status=apt_data['status'],
                doctor_notes=apt_data['notes'],
            )

            # Create Invoice
            fee = apt_data['doctor'].consultation_fee
            inv = BillingInvoice.objects.create(
                appointment=apt,
                patient=apt_data['patient'],
                consultation_fee=fee,
                medicine_charges=Decimal('25.00') if apt_data['create_record'] else Decimal('0.00'),
                total_amount=fee + (Decimal('25.00') if apt_data['create_record'] else Decimal('0.00')),
                payment_status='paid' if apt_data['paid'] else 'unpaid',
                payment_method='card' if apt_data['paid'] else 'cash',
                paid_at=timezone.now() if apt_data['paid'] else None,
            )

            # Create Medical Record if completed
            if apt_data['create_record']:
                MedicalRecord.objects.create(
                    appointment=apt,
                    patient=apt_data['patient'],
                    doctor=apt_data['doctor'],
                    symptoms=apt_data['symptoms'],
                    diagnosis=apt_data['diagnosis'],
                    treatment_notes=apt_data['treatment_notes'],
                    prescribed_medicines=apt_data['rx'],
                    follow_up_date=apt_data['follow_up'],
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(sample_appointments)} appointments with records and invoices!"))
        self.stdout.write(self.style.SUCCESS("All seed data successfully generated!"))
