"""
URL configuration for the emission_app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('activity/', views.activity, name='activity'),
    path('history/', views.history, name='history'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('goals/', views.goals, name='goals'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
