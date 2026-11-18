from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, time
from decimal import Decimal

from accounts.models import User, PatientProfile
from hospital.models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


class Command(BaseCommand):
    help = 'Seeds database with realistic, professional hospital data (INR currency)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Initializing professional hospital database..."))

        # Clear existing data to maintain 100% clean relations
        Appointment.objects.all().delete()
        Doctor.objects.all().delete()

        # 1. Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@medicare.kerala.gov.in',
                'first_name': 'K. S.',
                'last_name': 'Radhakrishnan',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+91 94470 12345',
                'address': 'Kerala Medical Services Complex, Thiruvananthapuram - 695001'
            }
        )
        admin_user.first_name = 'K. S.'
        admin_user.last_name = 'Radhakrishnan'
        admin_user.set_password('Admin@1234')
        admin_user.role = 'admin'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"Administrator initialized: {admin_user.username}"))

        # 2. Clinical Departments
        depts_data = [
            {
                'name': 'Cardiology',
                'icon': 'bi-heart-pulse-fill',
                'description': 'Comprehensive cardiac care including interventional angiography, 2D echo, ECG, and preventative heart care.'
            },
            {
                'name': 'Pediatrics',
                'icon': 'bi-emoji-smile-fill',
                'description': 'Compassionate child healthcare, pediatric intensive care, growth monitoring, and routine vaccination.'
            },
            {
                'name': 'Orthopedics & Joint Care',
                'icon': 'bi-bandaid-fill',
                'description': 'Joint replacements, arthroscopy, sports injury recovery, fracture fixation, and musculoskeletal therapy.'
            },
            {
                'name': 'Neurology',
                'icon': 'bi-activity',
                'description': 'Advanced diagnostics and treatment for stroke, epilepsy, chronic migraines, and neuromuscular disorders.'
            },
            {
                'name': 'General Medicine',
                'icon': 'bi-hospital-fill',
                'description': 'Primary consultations, chronic disease management (diabetes, hypertension), and comprehensive wellness screening.'
            },
        ]

        departments = {}
        for d in depts_data:
            dept, _ = Department.objects.get_or_create(
                name=d['name'],
                defaults={
                    'icon': d['icon'],
                    'description': d['description'],
                    'is_active': True,
                }
            )
            dept.icon = d['icon']
            dept.description = d['description']
            dept.save()
            departments[d['name']] = dept
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(departments)} clinical departments."))

        # 3. Professional Specialist Doctors (Matching usernames)
        doctors_data = [
            {
                'username': 'dr_rajesh',
                'email': 'dr.rajesh@medicare.kerala.gov.in',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'dept': 'Cardiology',
                'specialization': 'Senior Interventional Cardiologist',
                'qualification': 'MBBS, MD (Medicine), DM (Cardiology)',
                'experience': 15,
                'fee': Decimal('800.00'),
                'room': 'OPD Block A - Room 204',
                'days': 'Mon, Wed, Fri',
                'time_slot': '09:00 AM - 01:00 PM',
                'bio': 'Dr. Rajesh Kumar has over 15 years of experience in clinical & interventional cardiology, with specialized expertise in coronary angiograms and hypertension management.'
            },
            {
                'username': 'dr_lakshmi',
                'email': 'dr.lakshmi@medicare.kerala.gov.in',
                'first_name': 'Lakshmi',
                'last_name': 'Nair',
                'dept': 'Pediatrics',
                'specialization': 'Consultant Pediatrician',
                'qualification': 'MBBS, DCH, MD (Pediatrics)',
                'experience': 11,
                'fee': Decimal('500.00'),
                'room': 'OPD Block B - Room 102',
                'days': 'Mon - Sat',
                'time_slot': '10:00 AM - 03:00 PM',
                'bio': 'Dr. Lakshmi Nair is an experienced pediatrician known for her warm approach with young children and expertise in pediatric developmental milestones and asthma.'
            },
            {
                'username': 'dr_arun',
                'email': 'dr.arun@medicare.kerala.gov.in',
                'first_name': 'Arun',
                'last_name': 'Thomas',
                'dept': 'Orthopedics & Joint Care',
                'specialization': 'Orthopedic & Arthroscopy Surgeon',
                'qualification': 'MBBS, MS (Orthopedics), MCh (Ortho)',
                'experience': 14,
                'fee': Decimal('750.00'),
                'room': 'OPD Block C - Room 301',
                'days': 'Tue, Thu, Sat',
                'time_slot': '09:30 AM - 02:00 PM',
                'bio': 'Dr. Arun Thomas specializes in minimally invasive joint surgery, sports injury rehabilitation, and total knee & hip arthroplasty.'
            },
            {
                'username': 'dr_suresh',
                'email': 'dr.suresh@medicare.kerala.gov.in',
                'first_name': 'Suresh',
                'last_name': 'Pillai',
                'dept': 'Neurology',
                'specialization': 'Chief Neurologist',
                'qualification': 'MBBS, MD, DM (Neurology)',
                'experience': 16,
                'fee': Decimal('900.00'),
                'room': 'OPD Block A - Room 305',
                'days': 'Mon, Tue, Thu',
                'time_slot': '10:00 AM - 02:30 PM',
                'bio': 'Dr. Suresh Pillai has managed over 10,000 neurological cases covering migraine relief, stroke recovery, neuropathy, and movement disorders.'
            },
            {
                'username': 'dr_deepa',
                'email': 'dr.deepa@medicare.kerala.gov.in',
                'first_name': 'Deepa',
                'last_name': 'Varma',
                'dept': 'General Medicine',
                'specialization': 'Senior Consultant Physician',
                'qualification': 'MBBS, MD (General Medicine)',
                'experience': 12,
                'fee': Decimal('450.00'),
                'room': 'OPD Block B - Room 105',
                'days': 'Mon - Fri',
                'time_slot': '09:00 AM - 04:00 PM',
                'bio': 'Dr. Deepa Varma focuses on preventive adult medicine, diabetes mellitus management, thyroid disorders, and infectious fevers.'
            }
        ]

        doctors = []
        for d in doctors_data:
            doc_user, _ = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'email': d['email'],
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'role': 'staff',
                    'is_staff': True,
                    'phone': '+91 94471 22334',
                }
            )
            doc_user.first_name = d['first_name']
            doc_user.last_name = d['last_name']
            doc_user.email = d['email']
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
                    'available_days': d['days'],
                    'available_time_slot': d['time_slot'],
                    'bio': d['bio'],
                    'is_available': True,
                }
            )
            doctor_obj.department = departments[d['dept']]
            doctor_obj.specialization = d['specialization']
            doctor_obj.qualification = d['qualification']
            doctor_obj.experience_years = d['experience']
            doctor_obj.consultation_fee = d['fee']
            doctor_obj.room_number = d['room']
            doctor_obj.available_days = d['days']
            doctor_obj.available_time_slot = d['time_slot']
            doctor_obj.bio = d['bio']
            doctor_obj.is_available = True
            doctor_obj.save()
            doctors.append(doctor_obj)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(doctors)} professional specialist doctors."))

        # 4. Realistic Patients
        patients_data = [
            {
                'username': 'rahul_k',
                'email': 'rahul.krishnan@gmail.com',
                'first_name': 'Rahul',
                'last_name': 'Krishnan',
                'phone': '+91 98471 23456',
                'blood_group': 'O+',
                'allergies': 'Penicillin',
                'history': 'Essential Hypertension under treatment since 2021',
                'address': 'Marine Drive, Kochi, Kerala - 682031'
            },
            {
                'username': 'ananya_m',
                'email': 'ananya.menon@gmail.com',
                'first_name': 'Ananya',
                'last_name': 'Menon',
                'phone': '+91 94470 65432',
                'blood_group': 'A+',
                'allergies': 'None',
                'history': 'Mild seasonal allergic bronchitis',
                'address': 'Mavoor Road, Kozhikode, Kerala - 673004'
            },
            {
                'username': 'george_k',
                'email': 'george.kurian@gmail.com',
                'first_name': 'George',
                'last_name': 'Kurian',
                'phone': '+91 97455 78901',
                'blood_group': 'B+',
                'allergies': 'Sulfa drugs',
                'history': 'Previous right knee arthroscopic repair in 2023',
                'address': 'Baker Junction, Kottayam, Kerala - 686001'
            }
        ]

        patients = []
        for p in patients_data:
            p_user, _ = User.objects.get_or_create(
                username=p['username'],
                defaults={
                    'email': p['email'],
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'role': 'patient',
                    'phone': p['phone'],
                    'address': p['address'],
                }
            )
            p_user.first_name = p['first_name']
            p_user.last_name = p['last_name']
            p_user.set_password('Patient@1234')
            p_user.role = 'patient'
            p_user.save()

            profile, _ = PatientProfile.objects.get_or_create(user=p_user)
            profile.blood_group = p['blood_group']
            profile.allergies = p['allergies']
            profile.medical_history = p['history']
            profile.emergency_contact_name = 'Family Contact'
            profile.emergency_contact_phone = '+91 94470 99999'
            profile.save()

            patients.append(p_user)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(patients)} patients."))

        # 5. Realistic Sample Appointments (INR Invoices & Medical Records)
        today = timezone.localdate()
        sample_appointments = [
            # 1. Today confirmed with Dr. Rajesh Kumar (Cardiology)
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'dept': doctors[0].department,
                'date': today,
                'time': time(10, 30),
                'reason': 'Routine blood pressure evaluation and post-exertional cardiac check-up.',
                'status': 'confirmed',
                'notes': 'Patient advised to bring recent fasting lipid profile and ECG records.',
                'create_record': False,
                'paid': False,
            },
            # 2. Today pending with Dr. Lakshmi Nair (Pediatrics)
            {
                'patient': patients[1],
                'doctor': doctors[1],
                'dept': doctors[1].department,
                'date': today,
                'time': time(14, 0),
                'reason': 'Annual growth monitoring, developmental assessment, and immunization check.',
                'status': 'pending',
                'notes': '',
                'create_record': False,
                'paid': False,
            },
            # 3. Completed visit with Dr. Suresh Pillai (Neurology)
            {
                'patient': patients[0],
                'doctor': doctors[3],
                'dept': doctors[3].department,
                'date': today - timedelta(days=5),
                'time': time(11, 0),
                'reason': 'Recurring throbbing headaches aggravated by prolonged monitor work.',
                'status': 'completed',
                'notes': 'Diagnosed episodic tension headache. Advised ergonomic posture and hydration.',
                'create_record': True,
                'symptoms': 'Bilateral frontal headache, neck muscle tightness, interrupted sleep.',
                'diagnosis': 'Episodic Tension-Type Headache with Cervical Strain',
                'rx': '1. Tab. Naproxen 250mg - 1 tablet as needed with food\n2. Tab. Magnesium Glycinate 400mg - 1 tablet at bedtime (30 days)\n3. Gentle cervical spine isometric exercises 10 mins daily',
                'treatment_notes': 'Maintain proper ergonomic monitor height. Ensure 2.5 liters daily water intake.',
                'follow_up': today + timedelta(days=25),
                'paid': True,
            },
            # 4. Completed visit with Dr. Deepa Varma (General Medicine)
            {
                'patient': patients[1],
                'doctor': doctors[4],
                'dept': doctors[4].department,
                'date': today - timedelta(days=10),
                'time': time(9, 30),
                'reason': 'Routine annual executive wellness health check-up.',
                'status': 'completed',
                'notes': 'Vitals within normal limits. Fasting glucose and HbA1c normal.',
                'create_record': True,
                'symptoms': 'General wellness check, occasional seasonal fatigue.',
                'diagnosis': 'Routine Health Evaluation - Normal Findings',
                'rx': '1. Tab. Vitamin D3 60,000 IU - Once weekly for 8 weeks\n2. Balanced diet rich in fresh greens, fruits, and hydration',
                'treatment_notes': 'Perform 30 minutes of moderate aerobic exercise 5 days a week.',
                'follow_up': today + timedelta(days=90),
                'paid': True,
            },
            # 5. Upcoming visit with Dr. Arun Thomas (Orthopedics)
            {
                'patient': patients[2],
                'doctor': doctors[2],
                'dept': doctors[2].department,
                'date': today + timedelta(days=3),
                'time': time(15, 30),
                'reason': 'Right knee joint review following sports training resumption.',
                'status': 'pending',
                'notes': '',
                'create_record': False,
                'paid': False,
            },
            # 6. Cancelled visit
            {
                'patient': patients[2],
                'doctor': doctors[0],
                'dept': doctors[0].department,
                'date': today - timedelta(days=2),
                'time': time(16, 0),
                'reason': 'Executive preventive check-up.',
                'status': 'cancelled',
                'notes': 'Patient requested cancellation due to outstation travel.',
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

            fee = apt_data['doctor'].consultation_fee
            med_charge = Decimal('300.00') if apt_data['create_record'] else Decimal('0.00')
            BillingInvoice.objects.create(
                appointment=apt,
                patient=apt_data['patient'],
                consultation_fee=fee,
                medicine_charges=med_charge,
                total_amount=fee + med_charge,
                payment_status='paid' if apt_data['paid'] else 'unpaid',
                payment_method='upi' if apt_data['paid'] else 'cash',
                paid_at=timezone.now() if apt_data['paid'] else None,
            )

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

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(sample_appointments)} appointments with clean INR invoices!"))
        self.stdout.write(self.style.SUCCESS("Database seeded with 100% clean, professional doctor profiles!"))
