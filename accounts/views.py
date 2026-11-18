from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegistrationForm, UserProfileUpdateForm, PatientProfileForm, UserAdminUpdateForm
from .models import User, PatientProfile
from .decorators import admin_required


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created successfully for {user.username}! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard_redirect_view(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    elif request.user.is_staff_member():
        return redirect('doctor_dashboard')
    else:
        return redirect('patient_dashboard')


@login_required
def profile_view(request):
    user = request.user
    patient_profile = None
    if user.is_patient():
        patient_profile, _ = PatientProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        p_form = PatientProfileForm(request.POST, instance=patient_profile) if patient_profile else None

        if u_form.is_valid() and (p_form is None or p_form.is_valid()):
            u_form.save()
            if p_form:
                p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        u_form = UserProfileUpdateForm(instance=user)
        p_form = PatientProfileForm(instance=patient_profile) if patient_profile else None

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_obj': user,
    }
    return render(request, 'accounts/profile.html', context)


@admin_required
def user_list_view(request):
    query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '').strip()

    users = User.objects.all().order_by('-date_joined')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    if role_filter:
        users = users.filter(role=role_filter)

    context = {
        'users': users,
        'query': query,
        'role_filter': role_filter,
    }
    return render(request, 'accounts/user_list.html', context)


@admin_required
def user_edit_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserAdminUpdateForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {target_user.username} updated successfully!")
            return redirect('user_list')
    else:
        form = UserAdminUpdateForm(instance=target_user)

    return render(request, 'accounts/user_edit.html', {'form': form, 'target_user': target_user})
