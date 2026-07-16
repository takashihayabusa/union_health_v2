from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("callback/", views.callback, name="callback"),

    path("users/", views.user_list, name="user_list"),

    path("register/", views.register, name="register"),

    path("send/", views.send_health_check, name="send_health_check"),

    path("emergency-send/", views.emergency_send, name="emergency_send"),

    path("line-logs/", views.line_logs, name="line_logs"),
    
    path(
        "clear-test-users/",
        views.clear_test_users,
        name="clear_test_users",
    ),
    path(
        "clear-all-users/",
        views.clear_all_users,
        name="clear_all_users",
    ),
    path(
    "export-logs/",
    views.export_logs_excel,
    name="export_logs",
    ),
    path(
    "delete-logs/",
    views.delete_logs,
    name="delete_logs",
    ),
    ] 