# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', home, name='home'),
    path('personnel_officer/', personnel_officer_dashboard, name='personnel_officer_dashboard'),
    path('personnel_officer_receptionist/', personnel_officer_receptionist, name='personnel_officer_receptionist'),
    path('personnel_officer_accountant/', personnel_officer_accountant, name='personnel_officer_accountant'),
    path('personnel_officer_calculator/', personnel_officer_calculator, name='personnel_officer_calculator'),
    path('personnel_officer_hard_worker/', personnel_officer_hard_worker, name='personnel_officer_hard_worker'),
    path('personnel_officer_storekeeper/', personnel_officer_storekeeper, name='personnel_officer_storekeeper'),
    path('personnel_officer_order/', personnel_officer_order, name='personnel_officer_order'),
    path('personnel_officer_edit_order/<int:order_id>/', personnel_officer_edit_order, name='personnel_officer_edit_order'),
    path('personnel_officer_receipt/', personnel_officer_receipt, name='personnel_officer_receipt'),
    path('personnel_officer_edit_receipt/<int:receipt_id>/', personnel_officer_edit_receipt, name='personnel_officer_edit_receipt'),
    path('admin_order_delete/<int:order_id>/', admin_delete_order, name='admin_delete_order'),
    path('admin_receipt_delete/<int:receipt_id>/', admin_delete_receipt, name='admin_delete_receipt'),
    path('add_receptionist/', add_receptionist, name='add_receptionist'),
    path('edit_receptionist/<int:receptionist_id>/', edit_receptionist, name='edit_receptionist'),
    path('delete_receptionist/<int:receptionist_id>/', delete_receptionist, name='delete_receptionist'),
    path('add_accountant/', add_accountant, name='add_accountant'),
    path('edit_accountant/<int:accountant_id>/', edit_accountant, name='edit_accountant'),
    path('delete_accountant/<int:accountant_id>/', delete_accountant, name='delete_accountant'),
    path('add_hard_worker/', add_hard_worker, name='add_hard_worker'),
    path('edit_hard_worker/<int:hard_worker_id>/', edit_hard_worker, name='edit_hard_worker'),
    path('delete_hard_worker/<int:hard_worker_id>/', delete_hard_worker, name='delete_hard_worker'),
    path('add_storekeeper', add_storekeeper, name='add_storekeeper'),
    path('edit_storekeeper/<int:storekeeper_id>/', edit_storekeeper, name='edit_storekeeper'),
    path('delete_storekeeper/<int:storekeeper_id>/', delete_storekeeper, name='delete_storekeeper'),
    path('add_calculator', add_calculator, name='add_calculator'),
    path('edit_calculator/<int:calculator_id>/', edit_calculator, name='edit_calculator'),
    path('delete_calculator/<int:calculator_id>/', delete_calculator, name='delete_calculator'),
]

