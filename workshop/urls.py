# workshop/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),
    path('receipt/<int:receipt_id>/', receipt_detail, name='receipt_detail'),
    path('workshop/<int:hard_worker_id>/', workshop, name='workshop'),
    path('workshop_list/<int:hard_worker_id>/', workshop_list, name='workshop_list'),
    path('workshop_edit_order/<int:order_id>/', workshop_edit_order, name='workshop_edit_order'),
]
