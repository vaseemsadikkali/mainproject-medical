from django.urls import path
from . import views

urlpatterns = [
    # Public & Directory
    path('', views.home_view, name='home'),
    path('doctors/', views.doctors_list_view, name='doctors_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail_view, name='doctor_detail'),
    path('departments/', views.departments_list_view, name='departments_list'),

    # Dashboards
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard_view, name='patient_dashboard'),

    # Appointments CRUD
    path('appointments/', views.appointment_list_view, name='appointment_list'),
    path('appointments/book/', views.appointment_book_view, name='appointment_book'),
    path('appointments/<int:appointment_id>/', views.appointment_detail_view, name='appointment_detail'),
    path('appointments/<int:appointment_id>/edit/', views.appointment_edit_view, name='appointment_edit'),
    path('appointments/<int:appointment_id>/status/', views.appointment_status_update_view, name='appointment_status_update'),
    path('appointments/<int:appointment_id>/delete/', views.appointment_delete_view, name='appointment_delete'),

    # Medical Records
    path('appointments/<int:appointment_id>/medical-record/create/', views.medical_record_create_view, name='medical_record_create'),
    path('medical-records/<int:record_id>/', views.medical_record_detail_view, name='medical_record_detail'),
    path('medical-records/<int:record_id>/edit/', views.medical_record_edit_view, name='medical_record_edit'),

    # Admin Department CRUD
    path('departments/create/', views.department_create_view, name='department_create'),
    path('departments/<int:dept_id>/edit/', views.department_edit_view, name='department_edit'),
    path('departments/<int:dept_id>/delete/', views.department_delete_view, name='department_delete'),

    # Admin Doctor CRUD
    path('doctors/create/', views.doctor_create_view, name='doctor_create'),
    path('doctors/<int:doctor_id>/edit/', views.doctor_edit_view, name='doctor_edit'),

    # Billing & Invoices
    path('invoices/<int:invoice_id>/', views.invoice_detail_view, name='invoice_detail'),
    path('invoices/<int:invoice_id>/pay/', views.invoice_pay_view, name='invoice_pay'),

    # Reports
    path('reports/', views.reports_view, name='reports'),
]
