from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/redirect/', views.dashboard_redirect_view, name='dashboard_redirect'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
]
