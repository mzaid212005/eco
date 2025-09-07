from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='staff_login'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('update-status/<int:issue_id>/', views.update_status, name='update_status'),
    path('publish-issue/<int:issue_id>/', views.publish_issue, name='publish_issue'),
    path('manage-rewards/', views.manage_rewards, name='manage_rewards'),
    path('allot-reward/', views.allot_reward, name='allot_reward'),
    path('update-reward-status/<int:reward_id>/', views.update_reward_status, name='update_reward_status'),
]