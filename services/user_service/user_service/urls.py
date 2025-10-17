"""
URL configuration for user service API
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('users/', views.create_user, name='create_user'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/list/', views.list_users, name='list_users'),
    path('auth/login/', views.authenticate_user, name='authenticate_user'),
]