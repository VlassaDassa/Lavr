from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.main_page, name="main"),
    path('auth', views.auth_page, name="auth"),
    path('question/<id>/<question_number>', views.question_page, name="question"),
    path('auth_data', views.auth_data, name="auth_data"),
    path('save_user_answer', views.save_user_answer, name="save_user_answer"),
    path('save_user_test', views.save_user_test, name="save_user_test"),
    path('report_by_code', views.report_by_code, name="report_by_code"),
    path('check_success_test', views.check_success_test, name="check_success_test"),

    path('get_allow_tests', views.get_allow_tests, name="get_allow_tests"),
]
