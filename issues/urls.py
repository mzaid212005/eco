from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('public-board/', views.public_board, name='public_board'),
    path('accept-issue/<int:issue_id>/', views.accept_issue, name='accept_issue'),
    path('resolve-issue/<int:issue_id>/', views.resolve_issue, name='resolve_issue'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]