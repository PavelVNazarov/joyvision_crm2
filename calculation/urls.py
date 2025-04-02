# calculation/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('calculation_list/<int:calculator_id>/', calculation_list, name='calculation_list'),
    path('edit_calculation/<int:order_id>/', edit_calculation, name='edit_calculation'),
    path('calculation/<int:calculator_id>/', calculation, name='calculation'),
]
