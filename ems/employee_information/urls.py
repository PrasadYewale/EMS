from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('', views.main, name="main"),
    path('home', views.home, name="home-page"),

    path('ulogin', auth_views.LoginView.as_view(
        template_name='employee_information/login.html', redirect_authenticated_user=True), name="ulogin"),


    path('login', auth_views.LoginView.as_view(
        template_name='employee_information/login.html', redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    path('about', views.about, name="about-page"),
    path('departments', views.departments, name="department-page"),
    path('manage_departments', views.manage_departments,
         name="manage_departments-page"),
    path('save_department', views.save_department, name="save-department-page"),
    path('delete_department', views.delete_department, name="delete-department"),
    path('positions', views.positions, name="position-page"),
    path('manage_positions', views.manage_positions,
         name="manage_positions-page"),
    path('save_position', views.save_position, name="save-position-page"),
    path('delete_position', views.delete_position, name="delete-position"),
    path('employees', views.employees, name="employee-page"),
    path('manage_employees', views.manage_employees,
         name="manage_employees-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete-employee"),
    path('view_employee', views.view_employee, name="view-employee-page"),

    path('activity', views.activity, name="activity-page"),
    path('manage_activity', views.manage_activity, name="manage_activity-page"),
    path('save_activity', views.save_activity, name="save-activity-page"),
    path('delete_activity', views.delete_activity, name="delete-activity-page"),


    path('activity_rules', views.activity_rules, name="activity_rules-page"),
    path('manage_activity_rules', views.manage_activity_rules,
         name="manage_activity_rules-page"),
    path('save_activity_rules', views.save_activity_rules,
         name="save-activity_rules-page"),
    path('delete_activity_rules', views.delete_activity_rules,
         name="delete-activity_rules-page"),

    path('scores', views.scores, name="scores-page"),
    path('manage_scores', views.manage_scores, name="manage_scores-page"),
    path('save_scores', views.save_scores, name="save-scores-page"),
    path('delete_scores', views.delete_scores, name="delete-scores-page"),
    # path('points', views.points, name="points-page"),
    # path('product', views.product, name="product-page"),
    # path('scores', views.scores, name="scores-page")

    # ========================
    # users
    # =======================
    path('uslogin', views.login_view, name='uslogin'),
    path('pro/<str:email>', views.pro, name='pro'),
]
