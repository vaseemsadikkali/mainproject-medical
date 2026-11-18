from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not request.user.is_admin():
            messages.error(request, "Access denied: Administrator privileges required.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def staff_or_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not (request.user.is_staff_member() or request.user.is_admin()):
            messages.error(request, "Access denied: Staff or Doctor access required.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def patient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not request.user.is_patient():
            messages.error(request, "Access restricted to patients/general users.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles):
    """
    Decorator for views that checks that the user is logged in and has one of the allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Please log in to continue.")
                return redirect('login')
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to view this resource.")
            return redirect('dashboard_redirect')
        return _wrapped_view
    return decorator
