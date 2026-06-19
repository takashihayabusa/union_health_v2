from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name='home'),

path('callback/', views.callback, name='callback'),

path('users/', views.user_list, name='user_list'),

path('send/', views.send_health_check, name='send_health_check'),

path('emergency-send/', views.emergency_send, name='emergency_send'),

path('line-logs/', views.line_logs, name='line_logs'),

path('register/', views.register, name='register'),
]
