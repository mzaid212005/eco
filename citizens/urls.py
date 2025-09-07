from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='citizen_register'),
    path('login/', views.login_view, name='citizen_login'),
    path('dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('report-issue/', views.report_issue, name='report_issue'),
]