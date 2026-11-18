from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date, time
from decimal import Decimal

from accounts.models import User, PatientProfile
from hospital.models import Department, Doctor, Appointment, MedicalRecord, BillingInvoice


class Command(BaseCommand):
    help = 'Seeds database with Kerala-themed departments, doctors, patients, appointments, medical records, and INR invoices'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting Kerala Arogya Keralam database seed..."))

        # 1. Create Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@arogyakeralam.gov.in',
                'first_name': 'Dr. K. S.',
                'last_name': 'Radhakrishnan',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+91 94470 12345',
                'address': 'Kerala Health Mission Directorate, Thiruvananthapuram, Kerala - 695001'
            }
        )
        admin_user.set_password('Admin@1234')
        admin_user.role = 'admin'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"Administrator ready: {admin_user.username}"))

        # 2. Kerala Departments (Modern & Ayurvedic Healthcare)
        depts_data = [
            {
                'name': 'Ayurveda & Panchakarma',
                'icon': 'bi-flower1',
                'description': 'Traditional Kerala Ayurvedic rejuvenation, Panchakarma detox, herbal healing, and holistic wellness.'
            },
            {
                'name': 'Cardiology',
                'icon': 'bi-heart-pulse',
                'description': 'Advanced cardiovascular care, coronary angiography, echocardiogram, and lifestyle heart disease management.'
            },
            {
                'name': 'Neurology',
                'icon': 'bi-brain',
                'description': 'Comprehensive diagnosis and treatment for brain, stroke care, epilepsy, and neurological rehabilitation.'
            },
            {
                'name': 'Pediatrics',
                'icon': 'bi-emoji-smile',
                'description': 'Child healthcare, neonatal care, developmental milestones, and routine immunization.'
            },
            {
                'name': 'Orthopedics & Joint Care',
                'icon': 'bi-bandaid',
                'description': 'Specialized orthopedic surgery, arthroscopy, joint replacement, and sports trauma rehabilitation.'
            },
            {
                'name': 'General Medicine',
                'icon': 'bi-hospital',
                'description': 'Primary healthcare, seasonal fever management, diabetes care, and lifestyle disease prevention.'
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
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(departments)} Kerala medical departments."))

        # 3. Kerala Specialist Doctors
        doctors_info = [
            {
                'username': 'dr_smith',
                'email': 'dr.harikrishnan@arogyakeralam.org',
                'first_name': 'Harikrishnan',
                'last_name': 'Nair',
                'dept': 'Cardiology',
                'specialization': 'Senior Interventional Cardiologist',
                'qualification': 'MBBS, MD, DM (Cardiology) - Govt. Medical College Trivandrum',
                'experience': 16,
                'fee': Decimal('800.00'),
                'room': 'Block A - Room 204',
                'bio': 'Dr. Harikrishnan Nair is a seasoned cardiologist with 16+ years of practice at Trivandrum & Kochi, specializing in preventative cardiology and vascular wellness.'
            },
            {
                'username': 'dr_sarah',
                'email': 'dr.ananya@arogyakeralam.org',
                'first_name': 'Ananya',
                'last_name': 'Menon',
                'dept': 'Pediatrics',
                'specialization': 'Consultant Pediatrician & Neonatologist',
                'qualification': 'MBBS, DCH, MD (Pediatrics) - Govt. Medical College Calicut',
                'experience': 10,
                'fee': Decimal('500.00'),
                'room': 'Block B - Room 108',
                'bio': 'Dr. Ananya Menon specializes in pediatric wellness, child developmental assessments, and childhood asthma prevention.'
            },
            {
                'username': 'dr_emily',
                'email': 'dr.fathima@arogyakeralam.org',
                'first_name': 'Fathima',
                'last_name': 'Rahiman',
                'dept': 'Neurology',
                'specialization': 'Chief Clinical Neurologist',
                'qualification': 'MBBS, MD, DM (Neurology) - Kochi Super Specialty Institute',
                'experience': 12,
                'fee': Decimal('850.00'),
                'room': 'Block A - Room 310',
                'bio': 'Dr. Fathima Rahiman has extensive clinical expertise in migraine management, stroke recovery, and neuromuscular disorders.'
            },
            {
                'username': 'dr_marcus',
                'email': 'dr.mathew@arogyakeralam.org',
                'first_name': 'Mathew',
                'last_name': 'Varghese',
                'dept': 'Orthopedics & Joint Care',
                'specialization': 'Orthopedic & Arthroscopic Surgeon',
                'qualification': 'MBBS, MS (Ortho) - GMC Kottayam, Fellow Arthroscopy UK',
                'experience': 15,
                'fee': Decimal('750.00'),
                'room': 'Block C - Room 102',
                'bio': 'Senior consultant specializing in knee & shoulder arthroscopy, joint replacement, and sports trauma recovery.'
            },
            {
                'username': 'dr_padmanabhan',
                'email': 'dr.padmanabhan@arogyakeralam.org',
                'first_name': 'Padmanabhan',
                'last_name': 'Vaidyan',
                'dept': 'Ayurveda & Panchakarma',
                'specialization': 'Ayurvedic Physician & Panchakarma Specialist',
                'qualification': 'BAMS, MD (Ayurveda) - Govt. Ayurveda College Thiruvananthapuram',
                'experience': 18,
                'fee': Decimal('600.00'),
                'room': 'Ayur Saukhyam - Room 001',
                'bio': 'Traditional Kerala Ayurvedic doctor with 18+ years of heritage healing in Panchakarma, arthritis treatment, and Rasayana therapy.'
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
                    'phone': '+91 94471 00000',
                }
            )
            doc_user.first_name = d['first_name']
            doc_user.last_name = d['last_name']
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
            doctor_obj.department = departments[d['dept']]
            doctor_obj.specialization = d['specialization']
            doctor_obj.qualification = d['qualification']
            doctor_obj.consultation_fee = d['fee']
            doctor_obj.room_number = d['room']
            doctor_obj.save()
            doctors.append(doctor_obj)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(doctors)} Kerala specialist doctors."))

        # 4. Kerala Patient Profiles
        patients_info = [
            {
                'username': 'john_doe',
                'email': 'rahul.chandran@gmail.com',
                'first_name': 'Rahul',
                'last_name': 'Chandran',
                'phone': '+91 98471 23456',
                'blood_group': 'O+',
                'allergies': 'Penicillin, Dust allergies',
                'history': 'Hypertension under management since 2021',
                'address': 'Flat 4B, Marine Drive Towers, Kochi, Kerala - 682031'
            },
            {
                'username': 'lisa_wong',
                'email': 'deepa.nambiar@gmail.com',
                'first_name': 'Deepa',
                'last_name': 'Nambiar',
                'phone': '+91 94470 65432',
                'blood_group': 'A+',
                'allergies': 'None',
                'history': 'Mild seasonal allergic rhinitis',
                'address': 'Nambiar Kovilakam, Mavoor Road, Kozhikode, Kerala - 673004'
            },
            {
                'username': 'david_miller',
                'email': 'george.joseph@gmail.com',
                'first_name': 'George',
                'last_name': 'Joseph',
                'phone': '+91 97455 78901',
                'blood_group': 'B+',
                'allergies': 'Sulfa drugs',
                'history': 'Right knee meniscus arthroscopy in 2023',
                'address': 'Kallara House, Baker Junction, Kottayam, Kerala - 686001'
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
            profile.emergency_contact_name = 'Sujatha ' + p['last_name']
            profile.emergency_contact_phone = '+91 94470 99999'
            profile.save()

            patients.append(p_user)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(patients)} Kerala patients."))

        # 5. Sample Appointments with INR Invoices & Prescriptions
        # Clean existing sample appointments to reload cleanly
        Appointment.objects.all().delete()
        today = timezone.localdate()

        sample_appointments = [
            # 1. Today's confirmed Cardiology appointment in Kochi
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'dept': doctors[0].department,
                'date': today,
                'time': time(10, 30),
                'reason': 'Blood pressure review and routine ECG examination at Kochi Clinic.',
                'status': 'confirmed',
                'notes': 'Advised patient to bring prior reports from Ernakulam General Hospital.',
                'create_record': False,
                'paid': False,
            },
            # 2. Today's pending Pediatrics appointment with Dr. Ananya Menon
            {
                'patient': patients[1],
                'doctor': doctors[1],
                'dept': doctors[1].department,
                'date': today,
                'time': time(14, 0),
                'reason': 'Pediatric annual growth monitoring and MMR vaccination checkup.',
                'status': 'pending',
                'notes': '',
                'create_record': False,
                'paid': False,
            },
            # 3. Completed past appointment with Dr. Fathima Rahiman
            {
                'patient': patients[0],
                'doctor': doctors[2],
                'dept': doctors[2].department,
                'date': today - timedelta(days=6),
                'time': time(11, 0),
                'reason': 'Recurring tension headaches exacerbated by coastal humidity and screen work.',
                'status': 'completed',
                'notes': 'Diagnosed tension cephalalgia, advised lifestyle modifications and stress management.',
                'create_record': True,
                'symptoms': 'Throbbing frontal headache, neck stiffness, disturbed sleep.',
                'diagnosis': 'Tension Cephalalgia with Mild Cervical Spasm',
                'rx': '1. Tab. Naproxen 250mg - 1 tablet SOS after food\n2. Tab. Magnesium Glycinate 400mg - 1 tablet at night (30 days)\n3. Kerala Ayurvedic Ksheerabala 101 Tailam - 2 drops Nasya morning',
                'treatment_notes': 'Perform gentle cervical stretches daily. Ensure 3 liters of tender coconut water or boiled cumin water daily.',
                'follow_up': today + timedelta(days=24),
                'paid': True,
            },
            # 4. Completed past appointment with Dr. Padmanabhan Vaidyan (Ayurveda)
            {
                'patient': patients[1],
                'doctor': doctors[4],
                'dept': doctors[4].department,
                'date': today - timedelta(days=12),
                'time': time(9, 30),
                'reason': 'Traditional Kerala Ayurvedic consultation for joint stiffness and Rasayana wellness.',
                'status': 'completed',
                'notes': 'Vata imbalance diagnosed, prescribed traditional Kashayam and Abhyangam.',
                'create_record': True,
                'symptoms': 'Morning stiffness in knee joints, fatigue, digestive sluggishness.',
                'diagnosis': 'Vata-Kapha Sandhigata Vata (Early Knee Osteoarthritis)',
                'rx': '1. Sahacharadi Kashayam - 15ml with 45ml lukewarm water twice daily before meals\n2. Yogaraja Guggulu - 1 tablet twice daily after meals\n3. Mahanarayana Thailam - Warm application over knees followed by hot fomentation',
                'treatment_notes': 'Recommended 7-day Abhyanga & Njavara Kizhi session at Arogya Keralam Ayur Center.',
                'follow_up': today + timedelta(days=20),
                'paid': True,
            },
            # 5. Upcoming Orthopedic visit with Dr. Mathew Varghese
            {
                'patient': patients[2],
                'doctor': doctors[3],
                'dept': doctors[3].department,
                'date': today + timedelta(days=3),
                'time': time(15, 30),
                'reason': 'Follow-up assessment after sports knee recovery.',
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
                'date': today - timedelta(days=3),
                'time': time(16, 0),
                'reason': 'Executive health check-up consultation.',
                'status': 'cancelled',
                'notes': 'Rescheduled due to travel to Kozhikode.',
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

            # Create INR Invoice
            fee = apt_data['doctor'].consultation_fee
            med_charges = Decimal('350.00') if apt_data['create_record'] else Decimal('0.00')
            BillingInvoice.objects.create(
                appointment=apt,
                patient=apt_data['patient'],
                consultation_fee=fee,
                medicine_charges=med_charges,
                total_amount=fee + med_charges,
                payment_status='paid' if apt_data['paid'] else 'unpaid',
                payment_method='upi' if apt_data['paid'] else 'cash',
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

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(sample_appointments)} Kerala appointments with INR (₹) invoices!"))
        self.stdout.write(self.style.SUCCESS("Arogya Keralam Kerala database successfully initialized!"))
