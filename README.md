# Arogya Keralam (ആരോഗ്യകേരളം) – Kerala Healthcare Management System with Role-Based Access Control

A comprehensive, production-ready Django web application developed according to the **Entri Final Project Guidelines**. Built with an authentic **Kerala theme** ("God's Own Healthcare"), standard **Indian Rupee (INR - ₹)** currency integration, strict **Role-Based Access Control (RBAC)** across three distinct user roles, full CRUD workflows, interactive dashboards with Chart.js analytics, database relationships, and a responsive Bootstrap 5 UI.

---

## 1. Project Overview & Features

### 1.1 Three Core User Roles
1. **Admin (Full Control)**
   - Access to Admin Dashboard with real-time KPI metrics & Chart.js visualizations.
   - User Management: View all registered users, toggle account status, and assign/modify roles.
   - Clinical Administration: Full CRUD control over Medical Departments and Doctor profiles.
   - Financial & Appointment Reports: Filter records by department and date range with print/export view.
   - Standard Django Administration Panel (`/admin/`) with registered models, filters, and search.

2. **Staff / Doctor (Partial Control)**
   - Dedicated Doctor Workspace with today's patient schedule and upcoming queues.
   - Appointment Status Management: Confirm, complete, or reschedule consultation visits.
   - Clinical Diagnosis & Prescriptions: Issue digital prescriptions with dosage instructions and treatment notes.
   - File Uploads: Attach and review patient lab reports, scan documents, or radiology images.

3. **User / Patient (Basic Access)**
   - Public Directory: Browse specialist doctors and hospital departments.
   - Online Booking: Schedule appointments with preferred doctors, time slots, and consultation reasons.
   - Appointment Management: View upcoming and historical visits; edit or cancel pending bookings.
   - Medical Records & History: View and print digital prescriptions issued by attending physicians.
   - Invoices & Billing: Track consultation fees and complete simulated digital payments.

---

## 2. Technical Stack

- **Backend Framework:** Django (Python 3.10+)
- **Database:** SQLite (default, with foreign keys, cascading rules, and full migrations)
- **Frontend / UI:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons
- **Data Visualization:** Chart.js (interactive status distribution & department volume graphs)
- **Authentication:** Custom User model inheriting from `AbstractUser` with custom role decorators (`@admin_required`, `@staff_or_admin_required`, `@patient_required`)

---

## 3. Project Directory Structure

```text
final project/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── medicare_project/          # Project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # User Management & Authentication App (Module 1)
│   ├── models.py              # Custom User & PatientProfile
│   ├── views.py               # Login, Register, Profile, Admin User Management
│   ├── forms.py               # UserRegistrationForm, UserProfileUpdateForm
│   ├── urls.py
│   ├── decorators.py          # Role-based access control decorators
│   └── admin.py               # Custom UserAdmin configuration
│
├── hospital/                  # Main Functional Module & Dashboards (Modules 2 & 3)
│   ├── models.py              # Department, Doctor, Appointment, MedicalRecord, BillingInvoice
│   ├── views.py               # Dashboards, Appointments CRUD, Doctors, Depts, Reports
│   ├── forms.py               # AppointmentBookingForm, MedicalRecordForm, etc.
│   ├── urls.py
│   ├── admin.py               # Registered ModelAdmin configurations
│   ├── tests.py               # Automated test suite
│   └── management/
│       └── commands/
│           └── seed_data.py   # Seed command for demo data
│
├── templates/                 # Responsive HTML5 Templates
│   ├── base.html              # Common master layout with navigation & messages
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── user_list.html
│   │   └── user_edit.html
│   └── hospital/
│       ├── home.html
│       ├── dashboard_admin.html
│       ├── dashboard_doctor.html
│       ├── dashboard_patient.html
│       ├── doctors_list.html
│       ├── doctor_detail.html
│       ├── doctor_form.html
│       ├── department_list.html
│       ├── department_form.html
│       ├── department_confirm_delete.html
│       ├── book_appointment.html
│       ├── appointment_list.html
│       ├── appointment_detail.html
│       ├── appointment_edit.html
│       ├── appointment_status_update.html
│       ├── appointment_confirm_delete.html
│       ├── medical_record_form.html
│       ├── medical_record_detail.html
│       ├── invoice_detail.html
│       ├── invoice_pay.html
│       └── reports.html
│
├── static/                    # Custom static assets
│   ├── css/custom.css
│   └── js/main.js
│
└── media/                     # Upload directory for lab reports & profiles
    ├── profiles/
    └── medical_reports/
```

---

## 4. Credentials for Evaluation & Testing

The project comes pre-seeded with accounts for all three roles:

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@1234` | Full access, user management, charts, reports, Django admin |
| **Staff / Doctor** | `dr_smith` | `Doctor@1234` | Doctor workspace, today's schedule, issue prescriptions, file uploads |
| **Staff / Doctor** | `dr_sarah` | `Doctor@1234` | Pediatrician workspace, review appointments |
| **Patient / User** | `john_doe` | `Patient@1234` | Book visits, view history, print prescriptions, pay invoices |
| **Patient / User** | `lisa_wong` | `Patient@1234` | Patient portal, schedule consultations |

---

## 5. Quick Setup & Execution Guide

### Step 1: Clone or Navigate to the Project Directory
```bash
cd "c:\Users\vasee\OneDrive\Desktop\final project"
```

### Step 2: (Optional) Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Seed Demo Data (Departments, Doctors, Appointments, Users)
```bash
python manage.py seed_data
```

### Step 6: Run Automated Tests
```bash
python manage.py test
```

### Step 7: Launch the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 6. Verification of Guidelines Checklist

- [x] **User Authentication System:** User registration, login, logout, profile update.
- [x] **Role-Based Access Control:** 3 explicit roles (Admin, Staff/Doctor, Patient/User) strictly enforced via custom decorators and template conditionals.
- [x] **Full CRUD Operations:** Complete Create, Read, Update, and Delete operations implemented on Appointments, Medical Records, Departments, and Doctors.
- [x] **Core Modules:**
  1. User Management (Module 1: `/accounts/users/`, registration, login, profile)
  2. Main Functional Module (Module 2: Appointments, consultations, clinical prescriptions)
  3. Reports & Dashboards (Module 3: Role-specific dashboards, KPI cards, Chart.js graphs, filterable reports)
- [x] **UI & Responsiveness:** Built using HTML5, CSS3, and Bootstrap 5.3 with full mobile and desktop responsiveness.
- [x] **Security Requirements:** Login required on protected routes, Admin-only restriction, Doctor-only clinical restrictions.
- [x] **Database & Migrations:** SQLite with Foreign Keys, OneToOne relationships, and applied migrations.
- [x] **Django Admin Panel:** Models registered with custom `list_display`, `list_filter`, and `search_fields`.
- [x] **Additional Recommended Features:**
  - Search & filter functionality on appointments and doctors.
  - Interactive Chart.js dashboard charts.
  - File upload support for lab reports and profile pictures.
- [x] **Documentation:** Setup instructions, credentials, commands, and requirements.

---

## 7. Deployment Guidelines (Submission Link)

To deploy this project to platforms like **Render**, **Railway**, or **PythonAnywhere**:
1. Ensure `ALLOWED_HOSTS = ['*']` or specify your production domain in `medicare_project/settings.py`.
2. Set up environment variables for `SECRET_KEY` and `DEBUG = False`.
3. Add `gunicorn` to `requirements.txt` (`pip install gunicorn`).
4. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Complete MediCare Hub Django final project"
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```
5. Connect your GitHub repository to Render / Railway / PythonAnywhere and deploy!
