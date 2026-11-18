from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PatientProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'gender')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile Info', {
            'fields': ('role', 'phone', 'gender', 'date_of_birth', 'address', 'profile_picture')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Profile Info', {
            'fields': ('role', 'phone', 'gender', 'date_of_birth', 'address')
        }),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'emergency_contact_name', 'emergency_contact_phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'emergency_contact_name')
    list_filter = ('blood_group',)
