from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("callback/", views.callback, name="callback"),

    path("users/", views.user_list, name="user_list"),

    path("register/", views.register, name="register"),
    
    path("login/", views.login_view, name="login"),
    
    path("union-home/", views.union_home, name="union_home"),
    
    path("logout/", views.logout_view, name="logout"),

    path("send/", views.region_send, name="region_send"),
    
    path("send_health_check/", views.send_health_check, name="send_health_check"),
    
    path("emergency/", views.emergency_region, name="emergency_region"),

    path("emergency-send/", views.emergency_send, name="emergency_send"),

    path("line-logs/", views.line_logs, name="line_logs"),
    
    path("clear-test-users/", views.clear_test_users, name="clear_test_users"),
    
    path("clear-all-users/",views.clear_all_users,name="clear_all_users"),
    
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
    path(
    "account-register/",
    views.account_register,
    name="account_register",
    ),
    path(
    "accounts/",
    views.account_list,
    name="account_list",
    ),
    path(
    "accounts/<int:pk>/edit/",
    views.account_edit,
    name="account_edit",
    ),
    path(
    "accounts/<int:pk>/toggle/",
    views.account_toggle,
    name="account_toggle",
    ),

    path(
    "accounts/<int:pk>/delete/",
    views.account_delete,
    name="account_delete",
),
    path("protected-pdf/<str:filename>/", views.protected_pdf, name="protected_pdf"),
    path("signed-pdf/<str:filename>/", views.signed_pdf, name="signed_pdf"),
    
    path("union-news/", views.union_news, name="union_news"),
    path("mycar/", views.mycar, name="mycar"),
    path("roukin/", views.roukin, name="roukin"),
    path("consult/", views.consult, name="consult"),
    path("broadcast-history/", views.broadcast_history, name="broadcast_history"),
    path("broadcast-send/", views.broadcast_send, name="broadcast_send"),
    path("broadcast-pdf/<str:filename>/", views.broadcast_pdf, name="broadcast_pdf"),
    path("broadcast-pdf-file/<str:filename>/", views.broadcast_pdf_file, name="broadcast_pdf_file"),
    path("broadcast-test-send/", views.broadcast_test_send, name="broadcast_test_send"),
    path("broadcast-all-send/", views.broadcast_all_send, name="broadcast_all_send"),
    path("broadcast-all-confirm/", views.broadcast_all_confirm, name="broadcast_all_confirm"),
    ] 